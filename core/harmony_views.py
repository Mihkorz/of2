# -*- coding: utf-8 -*-

import os
import time
import pandas.rpy.common as com
import csv
import numpy as np
from pandas import DataFrame, Series, read_csv
from rpy2.robjects.packages import importr
from collections import defaultdict
        
from django import forms
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse 
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from .forms import ShambalaParametersForm, HarmonyParametersForm
from .stats import Shambhala_harmonisation, quantile_normalization
from profiles.models import ShambalaDocument

class ShambalaForm(FormView):
    form_class = ShambalaParametersForm
    template_name = 'core/shambala_form.html'
    success_url = '/shambala/done/'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ShambalaForm, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):        
        context = super(ShambalaForm, self).get_context_data(**kwargs)
        
        context['test'] = 'test'
        return context
    
    def form_valid(self, form):
        document = form.save(commit=False)
        document.created_by = self.request.user
        document.save()
        
        log_scale = form.cleaned_data.get('log_scale', False)
        
        auxiliary = form.cleaned_data.get('auxiliary', 'illumina') #default=illumina
        if auxiliary == 'illumina':
            df_p1 = read_csv(settings.MEDIA_ROOT+'/Shambala/ILL_AGL_abs.txt', sep=' ')
            df_p1.set_index('SYMBOL', inplace=True)
        if auxiliary == 'customar':
            df_p1 = read_csv(settings.MEDIA_ROOT+'/Shambala/CustomArray.txt', sep=' ')
            df_p1.set_index('SYMBOL', inplace=True)
        
        

        
        df_p = read_csv(settings.MEDIA_ROOT+'/'+document.document.name, sep=r'[\t, ;]')
        df_p.set_index('SYMBOL', inplace=True)
        
        document.doc_type = 1
        document.row_num = len(df_p)
        document.sample_num = len(df_p.columns)
        document.save()
        
        def normalize_with_p1(col):
           
            joined_df = DataFrame(col).join(df_p1, how='inner')
            
            joined_df = np.log(joined_df)
            column_names = joined_df.columns
            
            qn_df = quantile_normalization(joined_df)
            qn_df.set_index(0, inplace=True)
            qn_df.index.name = 'SYMBOL'
            qn_df.columns = column_names
            
            
            df_pl2 = DataFrame({})
            df_after_harmony = Shambhala_harmonisation(qn_df, df_pl2, harmony_type='harmony_afx_static', p1_names=0, p2_names=0,
                                 iterations=3, K=10, L=4, log_scale=log_scale, gene_cluster='skmeans',
                                 assay_cluster='hclust', corr='pearson', skip_match=False)
            
            
            return df_after_harmony[col.name]
        
        #result_df = df_p[df_p.columns[0:2]].apply(normalize_with_p1, axis=0)
        result_df = df_p.apply(normalize_with_p1, axis=0)
        
        output_doc = ShambalaDocument()        
        output_doc.doc_type = 2
        output_doc.created_by = self.request.user
        output_doc.related_doc = document
        
        """ Saving results to csv file and to database """
        path = os.path.join('Shambala', str(document.created_by))
        file_name = 'shambala_'+str(document.get_filename())        
        
        output_file = default_storage.save(settings.MEDIA_ROOT+"/"+path+"/"+file_name, ContentFile(''))
        
        result_df.to_csv(output_file)
        
        output_doc.document = path+"/"+os.path.basename(output_file)

        output_doc.save()
        
        
        return HttpResponseRedirect(reverse('shambala_done'))
        
    
    def form_invalid(self, form):
            return self.render_to_response(self.get_context_data(form=form))
        


class ShambalaDone(TemplateView):
    template_name = 'core/shambala_done.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ShambalaDone, self).dispatch(request, *args, **kwargs)
        
    
    def get_context_data(self, **kwargs):        
        context = super(ShambalaDone, self).get_context_data(**kwargs)
        context['documents'] =  ShambalaDocument.objects.all().order_by('-created_at')
         
        return context

class HarmonyForm(FormView):
    
    form_class = HarmonyParametersForm
    success_url = '/thanks/'
    
    template_name = 'core/harmonyform.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(HarmonyForm, self).dispatch(request, *args, **kwargs)
        
    
    def get_context_data(self, **kwargs):        
        context = super(HarmonyForm, self).get_context_data(**kwargs)
        
        context['test'] = 'test'
        return context
    
    def rename_df_columns(self, df):
        
        name_counts = defaultdict(int)
        new_col_names = []
            
        for name in df.columns:
            new_count = name_counts[name] + 1
            new_col_names.append("{}.{}".format(name, new_count))
            name_counts[name] = new_count 
                
            
        df.columns = new_col_names
        return df
    
    def form_valid(self, form):
        
        harmony_type=self.request.POST.get('harmony_type', False)
        
        pl1 = form.cleaned_data.get('pl1', False)
        pl2 = form.cleaned_data.get('pl2', False)
        k = form.cleaned_data.get('k', 10)
        l = form.cleaned_data.get('l', 4)
        log_scale = form.cleaned_data.get('log_scale', True)
        p1_names = form.cleaned_data.get('p1_names', 0)
        p2_names = form.cleaned_data.get('p2_names', 0)
        gene_cluster = form.cleaned_data.get('gene_cluster', 'kmeans')
        assay_cluster = form.cleaned_data.get('assay_cluster', 'kmeans')
        corr = form.cleaned_data.get('corr', 'pearson')
        iterations = form.cleaned_data.get('iterations', 30)
        skip_match = form.cleaned_data.get('skip_match', False) 
        
        sniffer = csv.Sniffer()
        dialect_pl1 = sniffer.sniff(pl1.read(), delimiters='\t,; ') # defining the separator of the csv file
        pl1.seek(0)
        df_pl1 = read_csv(pl1, delimiter=dialect_pl1.delimiter, index_col=0)
        
        df_pl2 = DataFrame({})
        if not "afx" in harmony_type:
            dialect_pl2 = sniffer.sniff(pl2.read(), delimiters='\t,; ') # defining the separator of the csv file
            pl2.seek(0)
            df_pl2 = read_csv(pl2, delimiter=dialect_pl2.delimiter, index_col=0)
        
        try:
            df_after_harmony = Shambhala_harmonisation(df_pl1, df_pl2, harmony_type=harmony_type, p1_names=p1_names, p2_names=p2_names,
                                 iterations=iterations, K=k, L=l, log_scale=log_scale, gene_cluster=gene_cluster,
                                 assay_cluster=assay_cluster, corr=corr, skip_match=skip_match)
        except:
            raise
        
        #raise Exception('harmony')
    
        
        if not "afx" in harmony_type:
            filename = pl1.name+pl2.name+".csv"
        else:
            filename = pl1.name+".csv"
        output_file = settings.MEDIA_ROOT+"/XPN/"+filename
        
        df_after_harmony.to_csv(output_file) 
        
        return HttpResponseRedirect(reverse('harmony_done', args=[filename]))
        
    
    def form_invalid(self, form):
            return self.render_to_response(self.get_context_data(form=form))
        
        
class HarmonyDone(TemplateView):
    template_name = 'core/harmonydone.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(HarmonyDone, self).dispatch(request, *args, **kwargs)
        
    
    def get_context_data(self, **kwargs):        
        context = super(HarmonyDone, self).get_context_data(**kwargs)
        output_file = self.args[0]
        context['output_file'] = output_file
        return context
    
class PrevFile:
    pass

class HarmonyPrevFiles(TemplateView):
    template_name = 'core/harmonyprevfiles.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(HarmonyPrevFiles, self).dispatch(request, *args, **kwargs)
        
    
    def get_context_data(self, **kwargs):
                
        context = super(HarmonyPrevFiles, self).get_context_data(**kwargs)
        path = settings.MEDIA_ROOT+"/XPN/"
        dirs = os.listdir(path)
        lFiles = []
        for files in dirs:
            f = PrevFile()
            stat = os.stat(settings.MEDIA_ROOT+"/XPN/"+files)
            f.name = files
            f.created = time.ctime(stat.st_ctime)
            f.size = stat.st_size/1048576
            lFiles.append(f)
            
        lFiles.sort(key=lambda x: x.created, reverse=True)
        context['filelist'] = lFiles       
        
        
        
        return context 
    
from database.models import Pathway, Gene    
from medic.models import Nosology, TreatmentMethod, TreatmentNorms
from core.stats import quantile_normalization, XPN_normalisation, fdr_corr
from scipy.stats.mstats import gmean
from scipy.stats import ttest_1samp, norm as scipynorm
from sklearn.metrics import roc_auc_score   
class breastmodule(TemplateView):
    template_name = 'core/breast.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(breastmodule, self).dispatch(request, *args, **kwargs)
        
    
    def get_context_data(self, **kwargs):
        context = super(breastmodule, self).get_context_data(**kwargs)
        """
          'GSE20271_GSE9475_normalized_Pac_ERN_HER2N_nonresponders.txt': 'GSE20271_GSE9475_normalized_Pac_ERN_HER2N_responders.txt',
          'GSE20194_GSE9574_normalized_ERP_HER2N_nonresponders.txt': 'GSE20194_GSE9574_normalized_ERP_HER2N_responders.txt', 
          'GSE20194_GSE9574_normalized_ERN_HER2P_nonresponders.txt': 'GSE20194_GSE9574_normalized_ERN_HER2P_responders.txt',
          'GSE20194_GSE9574_normalized_ERN_HER2N_nonresponders.txt': 'GSE20194_GSE9574_normalized_ERN_HER2N_responders.txt',
          'GSE18864_GSE42568_normalized_nonresponders.txt': 'GSE18864_GSE42568_normalized_responders.txt',
          'GSE18728_GSE42568_normalized.HER2N_nonresponders.txt': 'GSE18728_GSE42568_normalized.HER2N_responders.txt',#marker
          'GSE5462_GSE9574_normalized_nonresponders.txt': 'GSE5462_GSE9574_normalized_responders.txt' 
          
          'GSE50948_GSE42568_normalized_ERN_HER2P_TMB_nonresponders.txt': 'GSE50948_GSE42568_normalized_ERN_HER2P_TMB_responders.txt',
          'GSE50948_GSE42568_normalized_ERN_HER2P_nonresponders.txt': 'GSE50948_GSE42568_normalized_ERN_HER2P_responders.txt',
          'GSE50948_GSE42568_normalized_ERN_HER2N_nonresponders.txt': 'GSE50948_GSE42568_normalized_ERN_HER2N_responders.txt',
          'GSE48905_GSE42568_normalized_nonresponders.txt': 'GSE48905_GSE42568_normalized_responders.txt',
          'GSE42822_GSE9574_TMB_normalized_ERN_nonresponders.txt': 'GSE42822_GSE9574_TMB_normalized_ERN_responders.txt',
          'GSE42822_GSE9574_normalized_HER2N.ERP_nonresponders.txt': 'GSE42822_GSE9574_normalized_HER2N.ERP_responders.txt',
          'GSE42822_GSE9574_normalized_HER2N.ERN_nonresponders.txt': 'GSE42822_GSE9574_normalized_HER2N.ERN_responders.txt',
          'GSE41998_GSE10797_Paclitaxel_ERP.HER2N.nonresponders.txt': 'GSE41998_GSE10797_Paclitaxel_ERP.HER2N.responders.txt',
          'GSE41998_GSE10797_Paclitaxel_ERN.HER2N.nonresponders.txt': 'GSE41998_GSE10797_Paclitaxel_ERN.HER2N.responders.txt',
          'GSE41998_GSE10797_Ixabepilone_ERP.HER2N.nonresponders.txt': 'GSE41998_GSE10797_Ixabepilone_ERP.HER2N.responders.txt',
          'GSE41998_GSE10797_Ixabepilone_ERN.HER2N.nonresponders.txt': 'GSE41998_GSE10797_Ixabepilone_ERN.HER2N.responders.txt',
          'GSE41656_GSE32124_normalized_nonresponders.txt': 'GSE41656_GSE32124_normalized_responders.txt',
          'GSE37946_GSE9574_normalized_ERP_nonresponders.txt': 'GSE37946_GSE9574_normalized_ERP_responders.txt',
          'GSE37946_GSE9574_normalized_ERN_nonresponders.txt': 'GSE37946_GSE9574_normalized_ERN_responders.txt',
          'GSE34138_GSE32124_normalized_ERP_PRP_nonresponders.txt': 'GSE34138_GSE32124_normalized_ERP_PRP_responders.txt',
          'GSE34138_GSE32124_normalized_ERN_PRN_nonresponders.txt': 'GSE34138_GSE32124_normalized_ERN_PRN_responders.txt',
          'GSE33658_GSE42568_nonresponders.txt': 'GSE33658_GSE42568_responders.txt',
          'GSE32646_GSE42568_normalized_ERP.HER2N_nonresponders.txt': 'GSE32646_GSE42568_normalized_ERP.HER2N_responders.txt',
          'GSE32646_GSE42568_normalized_ERN.HER2P_nonresponders.txt' : 'GSE32646_GSE42568_normalized_ERN.HER2P_responders.txt',
          'GSE32646_GSE42568_normalized_ERN.HER2N_nonresponders.txt': 'GSE32646_GSE42568_normalized_ERN.HER2N_responders.txt',
          'GSE28844_GSE9574_normalized_nonresponders.txt': 'GSE28844_GSE9574_normalized_responders.txt',
          'GSE23988_GSE9574_normalized_ERP_nonresponders.txt': 'GSE23988_GSE9574_normalized_ERP_responders.txt',
          'GSE23988_GSE9574_normalized_ERN_nonresponders.txt': 'GSE23988_GSE9574_normalized_ERN_responders.txt',
          'GSE22513_GSE42568_nonresponders.txt': 'GSE22513_GSE42568_responders.txt',
          'GSE22358_normalized_HER2N_nonresponders.txt': 'GSE22358_normalized_HER2N_responders.txt',
          'GSE22093_GSE9574_normalized_ERP_nonresponders.txt': 'GSE22093_GSE9574_normalized_ERP_responders.txt',
          'GSE22093_GSE9574_normalized_ERN_nonresponders.txt': 'GSE22093_GSE9574_normalized_ERN_responders.txt',
          'GSE21974_GSE22820_normalized_HER2NP.ERN_nonresponders.txt': 'GSE21974_GSE22820_normalized_HER2N.ERN_responders.txt',
          """
        
        dFiles = {
          
          'GSE20271_GSE9475_normalized_Pac_ERN_HER2P_nonresponders.txt' : 'GSE20271_GSE9475_normalized_Pac_ERN_HER2P_responders.txt',
          
          
          }
        
        for nrfile, rfile in dFiles.iteritems():
            """ reading responders and non-resonders files """
            res_file_name = settings.MEDIA_ROOT+'/FilesForBCModule/'+rfile
            treatmentName = rfile.replace("_responders.txt", '')
            try:
                os.mkdir(settings.MEDIA_ROOT+'/noxpn/'+treatmentName)
            except:
                pass
            treatmentPath = settings.MEDIA_ROOT+'/noxpn/'+treatmentName
            with open(res_file_name, 'rb') as res_file:            
                sniffer = csv.Sniffer()
                dialect = sniffer.sniff(res_file.read(), delimiters='\t,;')
                res_file.seek(0)
                res_df = read_csv(res_file, delimiter=dialect.delimiter,
                                  index_col='SYMBOL') #create DataFrame for responders
                
                norms_columns =  [col for col in res_df.columns if 'Norm' in col]
                   
            nres_file_name = settings.MEDIA_ROOT+'/FilesForBCModule/'+nrfile
            with open(nres_file_name, 'rb') as nres_file:
                dialect = sniffer.sniff(nres_file.read(), delimiters='\t,;')
                nres_file.seek(0)
                nres_df = read_csv(nres_file, delimiter=dialect.delimiter,
                                   index_col='SYMBOL') #create DataFrame for non-responderss
                
            nres_df.drop(norms_columns, axis=1, inplace=True)
            joined_df = res_df.join(nres_df, how='inner') #merging 2 files together
            
            norms = TreatmentNorms.objects.filter(nosology_id=1)[0] #get norms for current cancer type
            
            tr_norms_df = read_csv(norms.file_norms_processed, index_col='SYMBOL')
            
            original_res_columns = [col for col in joined_df.columns if '_RES' in col]#store original column names
            len_o_r_c = len(original_res_columns)
            original_nres_columns = [col for col in joined_df.columns if '_NRES' in col]
            len_o_nr_c = len(original_nres_columns)
            original_resnres_columns = joined_df.columns 
            
            dict_marker = {}
            for counter in range(1): #100 XPN
                """ Performing XPN between norms and responders+non-responders""" 
                try:
                    pass
                    #df_after_xpn = XPN_normalisation(np.log(joined_df), np.log(tr_norms_df), iterations=30)
                except:
                    raise
                #raise Exception('breast')
                """ Performing PAS1 calculations for normalised DataFrame
                    filters: ttest_1samp + FDR correction 
                """
                df_for_pas1 = joined_df#np.exp(df_after_xpn[original_resnres_columns])
                
                all_genes = DataFrame(list(Gene.objects.values_list('name', flat=True).distinct())).set_index(0)
                all_genes.index.name = 'SYMBOL'
                df_for_pas1 = all_genes.join(df_for_pas1, how='inner')
                
                
                norms_df = df_for_pas1[[norm for norm in [col for col in df_for_pas1.columns if 'Norm' in col]]]
                norms_df = norms_df.abs().fillna(1)
                log_norms_df = np.log(norms_df)#use this for t-test, assuming log(norm) is distributed normally
                s_mean_norm = norms_df.apply(gmean, axis=1).fillna(1) #series of mean norms for CNR
            
                df_for_pas1.drop(norms_df.columns, axis=1, inplace=True)
                
                
                def apply_filter(col):
                    
                    _, p_value = ttest_1samp(log_norms_df, np.log(col), axis=1)
                    s_p_value = Series(p_value, index = col.index).fillna(0)
                    fdr_q_values = fdr_corr(np.array(s_p_value))
                    col[(fdr_q_values>=0.05)] = 0
                    
                    return col
            
                df_for_pas1 = df_for_pas1.apply(apply_filter, axis=0).fillna(0)
               
                df_for_pas1 = df_for_pas1.divide(s_mean_norm, axis=0).fillna(0) #acquire CNR values
                
                df_for_pas1.replace(0, 1, inplace=True)
                df_for_pas1 = df_for_pas1.abs()
                df_for_pas1 = np.log(df_for_pas1) # now we have log(CNR)
            
                pas1_all_paths = DataFrame()
                marker_pathways = []
            
                sample_names = []
                for col in df_for_pas1.columns:
                    sample_names+=[{'Sample': col, 'group': 'NonResponders' },
                                   {'Sample': col, 'group': 'Responders'}]
                df_probability = DataFrame(sample_names)
                
                """Start cycle """        
                for pathway in Pathway.objects.all().prefetch_related('gene_set'):
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
                        #if pathway.name == 'AKT_Pathway_Death_Genes':
                        #    raise Exception('AKT_Pathway_Death_Genes')
                        marker_pathways.append({'pathway': pathway.name,
                                                'AUC': AUC})
                pas1_all_paths.to_csv(treatmentPath+"/xpn_iter_"+str(counter)+".csv")
                dict_marker['iteration'+str(counter)] = marker_pathways
                print treatmentName+'.iteration '+str(counter)+' done \n'
                
            xpn_df = DataFrame(marker_pathways).fillna('')
            xpn_df.to_csv(treatmentPath+"/"+treatmentName+"_xpn_100.csv")
            
            #raise Exception('testing')  
        
        
        
        
        context['test'] = 'test'
        
        return context      
    
    
    