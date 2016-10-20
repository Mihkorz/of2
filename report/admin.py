# -*- coding: utf-8 -*-
import os
import csv
import pandas as pd
import numpy as np
from scipy.stats import ttest_1samp, ttest_ind
from scipy.stats.mstats import gmean

from django.contrib import admin
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from .models import Report, GeneGroup, PathwayGroup, TfGroup, DeepLearning
from core.stats import fdr_corr

class GeneGroupInline(admin.TabularInline):
    model = GeneGroup
    exclude = [ 'doc_boxplot']

class PathwayGroupInline(admin.TabularInline):
    model = PathwayGroup
    exclude = ['doc_proc',]

class TfGroupInline(admin.TabularInline):
    model = TfGroup
    
class DeepLearningInline(admin.TabularInline):
    model = DeepLearning
       
     
class ReportAdmin(admin.ModelAdmin):
    def targets_list(self):
        #return self.target_set.all()
        return ", ".join(target.name for target in self.target_set.all())
    list_display = ('title', 'organization', 'created_at')
    search_fields = ['title', 'organization']
    
        
    inlines = [
        GeneGroupInline,
        PathwayGroupInline,
        TfGroupInline,
        DeepLearningInline,
    ]
    
    def save_formset(self, request, form, formset, change):
        
        gene_groups = formset.save(commit=False)        
        
        for g_group in gene_groups:
            if g_group.__class__.__name__=='GeneGroup':
           
                print g_group.name
                sniffer = csv.Sniffer()
                dialect = sniffer.sniff(g_group.document.read(), delimiters='\t,; ')
                g_group.document.seek(0)
            
                df_doc = pd.read_csv(g_group.document, delimiter=dialect.delimiter,
                                 index_col='SYMBOL')
                tumour_columns = [col for col in df_doc.columns if 'Tumour' in col] #get sample columns 
                normal_columns = [col for col in df_doc.columns if 'Norm' in col] #get normal columns
            
            
                """ Creating DataFrame for doc_boxplot file """                    

                def boxplot(row):
            
                    sss = pd.Series()
            
                    r_norm = row.filter(like='Norm')
                    r_tumour = row.filter(like='Tumour')       
                
                    median = np.around(np.median(r_norm), decimals=0) 
                    upper_quartile = np.around(np.percentile(r_norm, 75), decimals=0)
                    lower_quartile = np.around(np.percentile(r_norm, 25), decimals=0)
                    iqr = upper_quartile - lower_quartile
                    upper_whisker = np.around(r_norm[r_norm<=upper_quartile+1.5*iqr], decimals=0).max()
                    lower_whisker = np.around(r_norm[r_norm>=lower_quartile-1.5*iqr], decimals=0).min()
                
                    sss['Normal_median'] = median
                    sss['Normal_upper_quartile'] = upper_quartile
                    sss['Normal_lower_quartile'] = lower_quartile
                    sss['Normal_upper_whisker'] = upper_whisker
                    sss['Normal_lower_whisker'] = lower_whisker
            
                    median = np.around(np.median(r_tumour), decimals=0) 
                    upper_quartile = np.around(np.percentile(r_tumour, 75), decimals=0)
                    lower_quartile = np.around(np.percentile(r_tumour, 25), decimals=0)
                    iqr = upper_quartile - lower_quartile
                    upper_whisker = np.around(r_tumour[r_tumour<=upper_quartile+1.5*iqr], decimals=0).max()
                    lower_whisker = np.around(r_tumour[r_tumour>=lower_quartile-1.5*iqr], decimals=0).min()
                
                    sss['Tumour_median'] = median
                    sss['Tumour_upper_quartile'] = upper_quartile
                    sss['Tumour_lower_quartile'] = lower_quartile
                    sss['Tumour_upper_whisker'] = upper_whisker
                    sss['Tumour_lower_whisker'] = lower_whisker
            
                    sss.name = row.name
                    return sss
            
            
                #df_boxplot = df_doc.apply(boxplot ,axis=1)
                print "Boxplot done"
                
                if not g_group.doc_logfc:
                    """ Creating DataFrame for doc_logFC file """
            
                    df_doc_log = np.log(df_doc.astype('float32')).fillna(0)
                    if len(tumour_columns)>1: # use group t-test
                    
                        def calculate_ttest(row):
                            tumours = row[tumour_columns]
                            norms = row[normal_columns]
                 
                            _, p_val = ttest_ind(tumours, norms)
                
                            return p_val
                
                        series_p_values = df_doc_log.apply(calculate_ttest, axis=1).fillna(1)
                        df_doc_log['P.Value'] = series_p_values
                
                        fdr_q_values = fdr_corr(np.array(series_p_values))
                        df_doc_log['adj.P.Val'] = fdr_q_values
            
                    else: # use single sample t-test
                        log_norms_df = df_doc_log[normal_columns]
                        def calculate_1sample_ttest(col):
                            _, p_value = ttest_1samp(log_norms_df, np.log(col), axis=1)
                            series_p_values = pd.Series(p_value, index = col.index).fillna(1)
                            df_doc_log['P.Value'] = series_p_values
                            fdr_q_values = fdr_corr(np.array(series_p_values))
                            df_doc_log['adj.P.Val'] = fdr_q_values
                    
                
                        df_doc_log[tumour_columns].apply(calculate_1sample_ttest, axis=0)
                
                
                    
                    cnr_gMean_norm = df_doc[normal_columns].apply(gmean, axis=1).fillna(1)
                    df_doc = df_doc.div(cnr_gMean_norm, axis='index')
                    cnr_gMean_tumour = df_doc[tumour_columns].apply(gmean, axis=1).fillna(1)
                    cnr_gMean_tumour = np.log2(cnr_gMean_tumour)
            
                    #combining all together
                    df_logfc = pd.DataFrame(index=df_doc.index)
                    df_logfc['logFC'] = cnr_gMean_tumour
                    df_logfc['adj.P.Val'] = df_doc_log['adj.P.Val']
                    df_logfc['P.Value'] = df_doc_log['P.Value']
                    print g_group.name+" logfc done"
            
            
                """ Saving to files and to database """
            
                path = os.path.join('report-portal', g_group.report.slug)
                if not g_group.doc_logfc:
                    file_logfc = default_storage.save(path+"/logfc_"+g_group.name+".csv", ContentFile('') )
                    df_logfc.to_csv(settings.MEDIA_ROOT+"/"+file_logfc)
                    g_group.doc_logfc = file_logfc
                
                #file_boxplot = default_storage.save(path+"/boxplot_"+g_group.name+".csv", ContentFile('') )
                #df_boxplot.to_csv(settings.MEDIA_ROOT+"/"+file_boxplot)
                
                #g_group.doc_boxplot = file_boxplot
                #raise Exception('group')
                g_group.save()
            elif g_group.__class__.__name__=='PathwayGroup':
                try:            
                    df_doc = pd.read_excel(g_group.document, sheetname='PAS1',
                                 index_col='Pathway')
                except:
                    g_group.document.seek(0)
                    df_doc = pd.read_csv(g_group.document, index_col='Pathway', encoding='utf-8')
                    
                tumour_columns = [col for col in df_doc.columns if 'Tumour' in col] #get sample columns
                
                mean = df_doc[tumour_columns].mean(1)
                df_doc['0'] = mean
                df_doc.drop([x for x in df_doc.columns if 'Tumour' in x ], axis=1, inplace=True)
                
                path = os.path.join('report-portal', g_group.report.slug)
                file_proc = default_storage.save(path+"/proc_"+g_group.name+".csv", ContentFile('') )
                df_doc.to_csv(settings.MEDIA_ROOT+"/"+file_proc, encoding='utf-8')
                g_group.doc_proc = file_proc
                
                g_group.save() # in case it's PathwayGroup object
            
            elif g_group.__class__.__name__=='TfGroup':
                
                #df_doc = pd.read_csv(g_group.document, sep=' ')
                
                #raise Exception('TF')
                
                g_group.save() # in case it's TfGroup object
            elif g_group.__class__.__name__=='DeepLearning':
                
                g_group.save()
        formset.save_m2m()

class GeneGroupAdmin(admin.ModelAdmin):
    fields = ['name','tip', 'drug']
    list_display = ('name', 'tip', 'drug')
    search_fields = ['name', 'drug__name']
    list_filter = ('drug__name',)


admin.site.register(Report, ReportAdmin)