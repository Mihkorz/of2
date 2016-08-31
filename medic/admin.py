# -*- coding: utf-8 -*-
import os
import csv
import numpy as np
from pandas import read_csv, DataFrame, Series
from scipy.stats.mstats import gmean
from scipy.stats import ttest_1samp, norm as scipynorm
from sklearn.metrics import roc_auc_score

from django.contrib import admin
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from .models import Nosology, TreatmentMethod, TreatmentNorms
from core.models import Pathway
from profiles.models import IlluminaProbeTarget
from core.stats import quantile_normalization, XPN_normalisation, fdr_corr, Shambhala_harmonisation


class NosologyAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Nosology, NosologyAdmin) 

class TreatmentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'nosology')
    
    def save_model(self, request, obj, form, change):
        
        def compute_jaccard_index(set_1, set_2):
            n = len(set(set_1).intersection(set_2))
            return n / float(len(set_1) + len(set_2) - n) 
        
        y_pred = []
        y_true = []
        #jjj = compute_jaccard_index(y_true, y_pred)
        #raise Exception('Jaccard')
        
        """ reading responders and non-resonders files """
        res_file = form.cleaned_data['file_res']
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(res_file.read(), delimiters='\t,;')
        res_file.seek(0)
        res_df = read_csv(res_file, delimiter=dialect.delimiter,
                          index_col='SYMBOL') #create DataFrame for responders
                
        nres_file = form.cleaned_data['file_nres']
        dialect = sniffer.sniff(nres_file.read(), delimiters='\t,;')
        nres_file.seek(0)
        nres_df = read_csv(nres_file, delimiter=dialect.delimiter,
                           index_col='SYMBOL') #create DataFrame for non-responderss
        
        nres_df.drop([x for x in nres_df.columns if 'Norm' in x], axis=1, inplace=True)
        
        joined_df = res_df.join(nres_df, how='inner') #merging 2 files together
        
        norms = TreatmentNorms.objects.filter(nosology=obj.nosology)[0] #get norms for current cancer type
        norms_df = read_csv(norms.file_norms_processed, index_col='SYMBOL')
        
        original_res_columns = [col for col in joined_df.columns if '_RES' in col]#store original column names
        len_o_r_c = len(original_res_columns)
        original_nres_columns = [col for col in joined_df.columns if '_NRES' in col]
        len_o_nr_c = len(original_nres_columns)
        len_r_nr = len_o_r_c+len_o_nr_c
        original_resnres_columns = joined_df.columns 
        #raise Exception(len_r_nr)
        
        """ Performing HARMONY between norms and responders+non-responders""" 
        try:
            #df_after_xpn = XPN_normalisation(joined_df, norms_df, iterations=30)
            df_pl2 = DataFrame({})
            """
            df_after_xpn=Shambhala_harmonisation(joined_df, df_pl2, harmony_type='harmony_afx_static', p1_names=0, p2_names=0,
                                 iterations=1, gene_cluster='skmeans', 
                                 assay_cluster='hclust', corr='pearson', skip_match=False)
            
            """
            df_after_xpn=Shambhala_harmonisation(joined_df, norms_df, harmony_type='harmony_static_equi', p1_names=0, p2_names=0,
                                 iterations=30, gene_cluster='kmeans', 
                                 assay_cluster='kmeans', corr='pearson', skip_match=False)
            
            print 'HARMONY DONE'
        except:
            raise
             
        #df_after_xpn = read_csv(settings.MEDIA_ROOT+"/xpn_done.csv", index_col='SYMBOL')
        
        """ Performing PAS1 calculations for normalised DataFrame
            filters: ttest_1samp + FDR correction 
        """
        df_for_pas1 = df_after_xpn[original_resnres_columns]
        
        norms_df = df_for_pas1[[norm for norm in [col for col in df_for_pas1.columns if 'Norm' in col]]]
        log_norms_df = np.log(norms_df)#use this for t-test, assuming log(norm) is distributed normally
        s_mean_norm = norms_df.apply(gmean, axis=1) #series of mean norms for CNR
            
        
        def apply_filter(col):
            _, p_value = ttest_1samp(log_norms_df, np.log(col), axis=1)
            s_p_value = Series(p_value, index = col.index).fillna(0)
            fdr_q_values = fdr_corr(np.array(s_p_value))
            col = col[(fdr_q_values<0.05)]
            return col
        
        df_for_pas1 = df_for_pas1.apply(apply_filter, axis=0).fillna(0)
        
        df_for_pas1 = df_for_pas1.divide(s_mean_norm, axis=0) #acquire CNR values
        df_for_pas1.replace(0, 1, inplace=True)
        df_for_pas1 = np.log(df_for_pas1) # now we have log(CNR)
        
        pas1_all_paths = DataFrame()
        marker_pathways = []
        marker_auc = []
        
        sample_names = []
        for col in df_for_pas1.columns:
            sample_names+=[{'Sample': col, 'group': 'NonResponders' },
                           {'Sample': col, 'group': 'Responders'}]
        df_probability = DataFrame(sample_names)
         
        """Start cycle """        
        for pathway in Pathway.objects.filter(organism='human', database='primary_old'):
            ar_probabilities = np.array([])            
            
            genes = DataFrame(list(pathway.gene_set.all()
                                      .values('name', 'arr'))).set_index('name')#fetch genes 
            
            genes.index.name = 'SYMBOL'
           
            joined = genes.join(df_for_pas1, how='inner').drop(['arr'], axis=1) 
            pas1_for_pathway = joined.apply(lambda x: x*genes['arr'].astype('float')).sum()            
            pas1_for_pathway = pas1_for_pathway.set_value('Pathway', pathway.name)
            pas1_for_pathway = DataFrame(pas1_for_pathway).T.set_index('Pathway')
            
            pas1_all_paths = pas1_all_paths.append(pas1_for_pathway)
            
            """ AUC calculations and determining Marker paths """
            df_res = pas1_for_pathway[original_res_columns]
            df_nres = pas1_for_pathway[original_nres_columns]
            arScore = np.append(np.array(df_res.values, dtype='float64'), np.array(df_nres.values, dtype='float64'))            
            arRes = np.ones(len_o_r_c)
            arNRes = np.zeros(len_o_nr_c)
            arTrue = np.append(arRes, arNRes)
            
            AUC = roc_auc_score(arTrue, arScore) #calculate AUC
            
            if AUC>0.7:
                marker_pathways.append(pathway.name)
                marker_auc.append(str(AUC))
                
                r_mean = df_res.mean(axis=1).values[0]
                r_std = df_res.std(axis=1).values[0]
                nr_mean = df_nres.mean(axis=1).values[0]
                nr_std = df_nres.std(axis=1).values[0]
                
        
                for col in pas1_for_pathway.columns:
                    pas1 = pas1_for_pathway[col].values[0]
                    if pas1 <= r_mean:
                        r_probability = scipynorm.cdf(pas1, r_mean, r_std)
                    else:
                        r_probability = 1- scipynorm.cdf(pas1, r_mean, r_std)
                    if pas1 <= nr_mean:
                        nr_probability = scipynorm.cdf(pas1, nr_mean, nr_std)
                    else:
                        nr_probability = 1- scipynorm.cdf(pas1, nr_mean, nr_std)
                    ar_probabilities = np.append(ar_probabilities, [nr_probability, r_probability ])
                    #raise Exception('from within a cycle')
                        

                df_probability[pathway.name] = Series(ar_probabilities, index=df_probability.index)
                
        path = os.path.join('medic', obj.nosology.name, obj.name)
        file_pas1 = default_storage.save(path+"/file_pas1.csv", ContentFile('') )
        file_probabilities = default_storage.save(path+"/file_probabilities.csv", ContentFile('') )
        pas1_all_paths.to_csv(settings.MEDIA_ROOT+"/"+file_pas1)
        df_probability.to_csv(settings.MEDIA_ROOT+"/"+file_probabilities)
        obj.file_pms1 = file_pas1
        obj.file_probability = file_probabilities      
        #mmmm = len(marker_pathways)
        #raise Exception('treatment')
        
        #obj.num_of_patients = 0 #delete this after migration
        #obj.accuracy = 0 #delete this after migration
        #obj.percentage_response = 0
        obj.save()    

admin.site.register(TreatmentMethod, TreatmentMethodAdmin)

class TreatmentNormsAdmin(admin.ModelAdmin):
    list_display = ('name', 'nosology', 'file_norms', 'num_of_norms', 'is_active')
    
    def save_model(self, request, obj, form, change):
        
        norm_file = form.cleaned_data['file_norms']
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(norm_file.read(), delimiters='\t,;')
        norm_file.seek(0)
        norm_df = read_csv(norm_file, delimiter=dialect.delimiter) #create DataFrame with Illumina probes
        try:
            norm_df.set_index('ID', inplace=True)
            norm_df.index.name = 'SYMBOL'
        except:
            norm_df.index.name = 'SYMBOL'
        norm_df = np.log2(norm_df)
        norm_columns = norm_df.columns
        
        qn_norm_df = quantile_normalization(norm_df) #quantile normalization
        qn_norm_df.set_index(0, inplace=True)
        qn_norm_df.index.name = 'SYMBOL'
        qn_norm_df.columns = norm_columns
        
        #qn_norm_df.to_csv(norm_file)
        
        obj.num_of_norms = len(norm_columns)        
          
        probetargets = DataFrame(list(IlluminaProbeTarget.objects.all()
                                      .values('PROBE_ID', 'TargetID')))#fetch Illumina probe-target mapping 
        probetargets.set_index('PROBE_ID', inplace=True)
        probetargets.index.name = 'SYMBOL'
        
        gene_norm_df = qn_norm_df.join(probetargets, how='inner')#Use intersection of keys from both frames
        gene_norm_df.set_index('TargetID', inplace=True)
        gene_norm_df = gene_norm_df.groupby(gene_norm_df.index, level=0).mean()#deal with duplicate genes by taking mean
        
        gene_norm_df.index.name = 'SYMBOL' #now we have DataFrame with gene symbols
        
        path = os.path.join('medic', obj.nosology.name, obj.name)
        file_processed = default_storage.save(path+"/pros_"+norm_file.name, ContentFile('') )
        gene_norm_df.to_csv(settings.MEDIA_ROOT+"/"+file_processed)
        
        obj.file_norms_processed = file_processed

        #raise Exception('test')
        
        obj.save()

admin.site.register(TreatmentNorms, TreatmentNormsAdmin) 


