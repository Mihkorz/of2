# -*- coding: utf-8 -*-
import os
import math
from datetime import datetime
from pandas import  DataFrame, Series, read_csv, read_excel,  ExcelWriter
import numpy as np
from scipy.stats.mstats import gmean
from scipy.stats import ttest_1samp, ttest_ind, ranksums

from django.views.generic.edit import FormView #CreateView , UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import MultipleObjectsReturned
from django.conf import settings

from .forms import  CalculationParametersForm, MedicCalculationParametersForm
from profiles.models import Document, ProcessDocument
from database.models import Pathway, Gene, Drug
from metabolism.models import MetabolismPathway, MetabolismGene
from mouse.models import MousePathway, MouseGene
from .stats import pseudo_ttest_1samp, fdr_corr


class CoreSetCalculationParameters(FormView):
    """
    Processes the form with calculation parameters, creates empty output Document, 
    creates Document in Process directory with PANDAS column 'Mean_Norm' and CNR for each gene     
    """
    
    template_name = 'core/core_calculation_parameters.html'
    success_url = '/success/'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        input_document = Document.objects.get(pk=self.kwargs['pk'])
        
        if input_document.project.field == 'med':
            self.form_class = MedicCalculationParametersForm
        else:
            self.form_class = CalculationParametersForm       
        return super(CoreSetCalculationParameters, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(CoreSetCalculationParameters, self).get_context_data(**kwargs)
        
        input_document = Document.objects.get(pk=self.kwargs['pk'])
                
        context['document'] = input_document
        return context
    
    def form_valid(self, form):
                
        context = self.get_context_data()
        
        """ update current Input Document """
        input_document = context['document']
        input_document.calculated_by = self.request.user
        input_document.calculated_at = datetime.now()
        input_document.save()        
                
        """ 
        Assigning values from Calculation parameters form and controlling defaults.
        variable = form.cleaned_data.get('name of field in form', 'Default value if not found in form')  
        """
        #filters
        use_ttest = form.cleaned_data.get('use_ttest', True)
        use_fdr = form.cleaned_data.get('use_fdr', True)
        use_ttest_1sam = form.cleaned_data.get('use_ttest_1sam', False) 
        pvalue_threshold = form.cleaned_data.get('pvalue_threshold', 0.05)
        qvalue_threshold = form.cleaned_data.get('qvalue_threshold', 0.05)        
        use_cnr = form.cleaned_data.get('use_cnr', True)
        cnr_low = form.cleaned_data.get('cnr_low', 0.67)
        cnr_up =  form.cleaned_data.get('cnr_up', 1.5)
        use_sigma = form.cleaned_data.get('use_sigma', False) # !!! deprecated !!! 
        sigma_num = form.cleaned_data.get('sigma_num', 2) # !!! deprecated !!!
        
        #database and normal choice
        norm_choice = form.cleaned_data.get('norm_choice', 2) #default=geometric
        db_choice = form.cleaned_data.get('db_choice', 1) #default=Human 
        
        #what to calculate and include in output report
        calculate_pas = form.cleaned_data.get('calculate_pas', False)
        calculate_pas1 = form.cleaned_data.get('calculate_pas1', True)
        calculate_pas2 = form.cleaned_data.get('calculate_pas2', False)
        calculate_ds1 = False #form.cleaned_data.get('calculate_ds1', False)
        calculate_ds2 = False #form.cleaned_data.get('calculate_ds2', False)
        calculate_ds3 = False #form.cleaned_data.get('calculate_ds3', False)
        calculate_norms_pas = form.cleaned_data.get('calculate_norms_pas', False)
        calculate_pvalue_each = form.cleaned_data.get('calculate_pvalue_each', False)
        calculate_pvalue_all = form.cleaned_data.get('calculate_pvalue_all', False)
        calculate_FDR_each = form.cleaned_data.get('calculate_FDR_each', False)
        calculate_FDR_all = form.cleaned_data.get('calculate_FDR_all', False)  
        new_pathway_names = form.cleaned_data.get('new_pathway_names', False)
        
        #From medical form. TODO: consider moving whole medical calculations to another view
        hormone_status = form.cleaned_data.get('hormone_status', False)
        her2_status = form.cleaned_data.get('her2_status', False)
        
        """ Create an empty Output Document  """
        
        if not os.path.exists(settings.MEDIA_ROOT+'/'+os.path.join('users', str(input_document.project.owner),
                                            str(input_document.project),'output')):
            os.mkdir(settings.MEDIA_ROOT+'/'+os.path.join('users', str(input_document.project.owner),
                                            str(input_document.project),'output'))
        
        output_doc = Document()        
        output_doc.doc_type = 2
        if int(db_choice) == 1:
            json_db = 'Human'
        elif int(db_choice) == 3:
            json_db = 'Mouse'
        elif int(db_choice) == 2:
            json_db = 'Metabolism'
        output_doc.parameters = {'sigma_num': sigma_num,
                                 'use_sigma': use_sigma,
                                 'cnr_low': cnr_low,
                                 'cnr_up': cnr_up,
                                 'use_cnr': use_cnr,
                                 'norm_algirothm': 'geometric' if int(norm_choice)>1 else 'arithmetic',
                                 'db': json_db,
                                 'hormone_status': hormone_status,
                                 'her2_status': her2_status }
        
        output_doc.project = input_document.project
        output_doc.created_by = self.request.user
        output_doc.created_at = datetime.now()        
        #output_doc.save()
                        
        
        """ Start Calculations"""
         
        def strip(text):
            try:
                return text.strip().upper()
            except AttributeError:
                return text
        
        calculate_p_value = False # Flag for p-value calculation
        
        process_doc_df = read_csv(settings.MEDIA_ROOT+"/"+input_document.input_doc.document.name,
                                  sep='\t', index_col='SYMBOL',  converters = {'SYMBOL' : strip}).fillna(0)        
        
        cnr_doc_df = process_doc_df # use to generate CNR file for downloading       
        tumour_columns = [col for col in process_doc_df.columns if 'Tumour' in col] #get sample columns 
        
        """ Standard T-test for genes """
        if use_ttest:

            def calculate_ttest(row):
                tumours = row[[t for t in row.index if 'Tumour' in t]]
                norms = row[[n for n in row.index if 'Norm' in n]]
                       
                _, p_val = ttest_ind(tumours, norms)
            
                return p_val
            log_process_doc_df = np.log(process_doc_df).fillna(0)
            series_p_values = log_process_doc_df.apply(calculate_ttest, axis=1).fillna(0)
            process_doc_df['p_value'] = series_p_values
            cnr_doc_df['p_value'] = series_p_values
            if use_fdr:
                fdr_q_values = fdr_corr(np.array(series_p_values))
                fdr_df = DataFrame({'p' : series_p_values,
                                    'q' : fdr_q_values
                                    })
                process_doc_df['q_value'] = fdr_df['q']
                cnr_doc_df['q_value'] = fdr_df['q']
                process_doc_df = process_doc_df[process_doc_df['q_value']<qvalue_threshold]
            else:
                process_doc_df = process_doc_df[process_doc_df['p_value']<pvalue_threshold]
        
        """ end of calculating horizontal p-values for genes """
         
        if input_document.norm_num >= 3:
            calculate_p_value = True                                
        
        pas_list = []
        pas1_list = []
        pas2_list = []
        differential_genes = {}
        
        if int(db_choice) == 1:
            pathway_objects = Pathway.objects.all() # Human DB
        elif int(db_choice) == 2:
            pathway_objects = MetabolismPathway.objects.all() # Metabolism DB
        elif int(db_choice) == 3:
            pathway_objects = MousePathway.objects.all() # Mouse DB
        #raise Exception('yoyoyo')
        """ START CYCLE """        
        for pathway in pathway_objects:
            gene_name = []
            gene_arr = []
            
            if int(db_choice) == 1:
                gene_objects = pathway.gene_set.all() # get Genes from Human DB
            elif int(db_choice) == 2:
                gene_objects = pathway.metabolismgene_set.all() # get Genes from Metabolism DB
            elif int(db_choice) == 3:
                gene_objects = pathway.mousegene_set.all() # get Genes from Mouse DB
                
            for gene in gene_objects:
                gene_name.append(gene.name.strip().upper())
                gene_arr.append(float(gene.arr))
            
            gene_data = {'SYMBOL': gene_name,
                         'ARR': gene_arr}
            
            gene_df = DataFrame(gene_data).set_index('SYMBOL')
            
            gene_df_abs = gene_df.abs() #for PAS2 calculation
            summ_genes_arr = (gene_df_abs['ARR'].sum() 
                              if gene_df_abs['ARR'].sum()>0 else 1) #for PAS2 calculation
            
            gene_df = gene_df.groupby(gene_df.index, level=0).mean() # take average value for duplicate genes 
            
            joined_df = gene_df.join(process_doc_df, how='inner') #intersect DataFrames to acquire only genes in current pathway
  
            pas_dict = {}
            pas1_dict = {}
            pas2_dict = {}
            
            pas_dict['Pathway'] = pas1_dict['Pathway'] = pas2_dict['Pathway'] = pathway.name.strip()
            
            """ Inserting new pathway names if needed """
            if new_pathway_names:
                new_path_df = read_excel(settings.MEDIA_ROOT+"/TRpathways_update_final_updated2.xlsx",
                                         sheetname=0,
                                         index_col='Old Pathway Name')            
                try:                    
                    new_path_name = new_path_df.loc[pathway.name.strip()][1] 
                except KeyError:
                    new_path_name = 'Unknown'
                    pass
                pas_dict['New pathway name'] = pas1_dict['New pathway name'] = pas2_dict['New pathway name'] = new_path_name
                
                
            
            """ Calculating PAS for samples and norms using filter(s)  """
            
            norms_df = joined_df[[norm for norm in [col for col in joined_df.columns if 'Norm' in col]]]
            log_norms_df = np.log(norms_df)#use this for t-test, assuming log(norm) is distributed normally
            
            """ get Series of mean norms for selected algorithm and std """
            if norm_choice>1: #geometric norms
                s_mean_norm = norms_df.apply(gmean, axis=1)
            else:             #arithmetic norms
                s_mean_norm = norms_df.mean(axis=1)
            std=norms_df.std(axis=1) # standard deviation
             
            def PAS1_calculation(col, arr):
                if ('Tumour' in col.name) or ('Norm' in col.name):
                    
                    col_CNR = col/s_mean_norm #convert column from GENE EXPRESSION to CNR
                    
                    if use_ttest_1sam: # two-sided 1sample T-test filter
                        _, p_value = ttest_1samp(log_norms_df, np.log(col), axis=1)
                        s_p_value = Series(p_value, index = col.index)
                        col_CNR = col_CNR[(s_p_value<pvalue_threshold)]
                                       
                    if use_cnr: # CNR FILTER
                        col_CNR = col_CNR[((col_CNR>cnr_up) | (col_CNR<cnr_low)) & (col_CNR>0)] 
                        
                    if use_sigma: # Sigma FILTER  !!! deprecated !!!                         
                        col_CNR = col_CNR[((col>=(s_mean_norm+sigma_num*std)) |
                                       (col<(s_mean_norm-sigma_num*std)))] 
                    
                    return np.log(col_CNR)*arr # PAS1=ARR*log(CNR)
                       
                else:
                    return col # in case it's not Tumour or Norm column
                
            pas_norms_samples = joined_df.apply(PAS1_calculation, axis=0, 
                                                  arr=joined_df['ARR'],
                                                ).fillna(0).sum()
             
            #raise Exception('exp') 
            lnorms_all = []
            lpas1_all = []
            for index, pas1 in pas_norms_samples.iteritems():
                if 'Norm' in index:
                    if calculate_p_value and (calculate_pvalue_each or calculate_pvalue_all):
                        lnorms_all.append(pas1)
                    if calculate_norms_pas:
                        pas_dict[index] = float(pathway.amcf)*pas1
                        pas1_dict[index] = pas1
                        pas2_dict[index] = pas1/summ_genes_arr
                    
                if 'Tumour' in index:
                    if calculate_pas:
                        pas_dict[index] = float(pathway.amcf)*pas1
                    if calculate_pas1:
                        pas1_dict[index] = pas1
                    if calculate_pas2:
                        pas2_dict[index] = pas1/summ_genes_arr
                    if calculate_p_value and calculate_pvalue_all:
                        lpas1_all.append(pas1)
            
            if calculate_p_value and calculate_pvalue_each:
                
                for index, pas1 in pas_norms_samples.iteritems():
                    if 'Tumour' in index:
                        _, p_val = pseudo_ttest_1samp(lnorms_all, pas1)
                        pas1_dict[index+'_p-value'] = p_val 
                                       
            
            if calculate_p_value and calculate_pvalue_all:
                     
                    _, p_val = ranksums(lnorms_all, lpas1_all)
                    pas1_dict['p-value_Mean'] = p_val                
            
            #raise Exception('exp') 
            """
            
            pms1_all = []
            for tumour in tumour_columns: #loop thought samples columns                
                summ = 0
                
                diff_genes_for_tumor = []
                for index, row in joined_df.iterrows():
                    if not use_sigma:
                        sigma_num = 0
                    if not use_cnr:
                        cnr_up = cnr_low = 0
                        
                    CNR = row[tumour]
                    if int(norm_choice) == 1:
                        mean = float(row['Mean_norm'])
                        EXPRESSION_LEVEL = CNR*float(mean)
                         
                    if int(norm_choice) == 2:
                        try:
                            mean = float(row['gMean_norm'])
                        except:
                            mean = 0 
                        EXPRESSION_LEVEL = CNR*float(mean)
                        
                    std = row['std'] if float(row['std'])>0 else 0   
                    if (
                        (
                           (EXPRESSION_LEVEL >= (mean + sigma_num*std)) or 
                           (EXPRESSION_LEVEL < (mean - sigma_num*std))
                         ) and 
                        (CNR > cnr_up or CNR < cnr_low) and 
                        (CNR > 0)
                       ):
                        
                        summ+= float(row['ARR'])*math.log(CNR) # ARR*ln(CNR)
                        
                        diff_genes_for_tumor.append(index.strip()) # store differential genes in a list
                if differential_genes.has_key(tumour):
                    differential_genes[tumour].extend(diff_genes_for_tumor)
                else:
                    differential_genes[tumour] = diff_genes_for_tumor
                    
                pms_dict[tumour] = float(pathway.amcf)*summ #PMS
                pms1_dict[tumour] = summ #PMS1
                pms2_dict[tumour] = summ/summ_genes_arr
                
                pms1_all.append(summ)
                
                if calculate_p_value and calculate_pvalue_each:
                    #from scipy.stats import ttest_1samp
                    from .stats import pseudo_ttest_1samp  
                    z_stat, p_val = pseudo_ttest_1samp(lnorms_p_value, summ)
                    pms1_dict[tumour+'_p-value'] = p_val               
            
            if calculate_p_value and calculate_pvalue_all:
                    from scipy.stats import ranksums  
                    z_stat, p_val = ranksums(lnorms_p_value, pms1_all)
                    pms1_dict['p-value_Mean'] = p_val 
        """        
            pas_list.append(pas_dict)
            pas1_list.append(pas1_dict)
            pas2_list.append(pas2_dict)        
        
        if calculate_pas:
            output_pas_df = DataFrame(pas_list)
            output_pas_df = output_pas_df.set_index('Pathway')
        if calculate_pas1:
            output_pas1_df = DataFrame(pas1_list)
            output_pas1_df = output_pas1_df.set_index('Pathway')
            
            if calculate_FDR_all:
                output_pas1_df['q-value_Mean'] = fdr_corr(np.array(output_pas1_df['p-value_Mean']))
            if calculate_FDR_each:
                col_p_val = [col for col in output_pas1_df.columns if '_p-value' in col]
                for col in col_p_val:
                    q_val_column_name = col.replace("_p-value", "_q-value");
                    output_pas1_df[q_val_column_name] = fdr_corr(np.array(output_pas1_df[col]))
                
            
        if calculate_pas2:
            output_pas2_df = DataFrame(pas2_list)
            output_pas2_df = output_pas2_df.set_index('Pathway')
        
        """ Calculating Drug Score """
        output_ds1_df = output_ds2_df = output_ds3_df = DataFrame()
        
        if (calculate_ds1 or calculate_ds2):
            ds1_list = []
            ds2_list = []
            ds3_list = []
        
            for drug in Drug.objects.all(): #iterate trough all Drugs
                ds1_dict = {}
                ds2_dict = {}
                ds3_dict = {}
                ds1_dict['Drug'] = ds2_dict['Drug'] = ds3_dict['Drug'] = drug.name.strip()
                ds1_dict['DataBase'] = ds2_dict['DataBase'] = ds3_dict['DataBase'] = drug.db
                ds1_dict['Type'] = ds2_dict['Type'] = ds3_dict['Type'] = drug.tip
            
            
            
                for tumour in tumour_columns: #loop thought samples columns
                    DS1 = 0 # DrugScore 1
                    DS2 = 0 # DrugScore 2
                    DS3 = 0
            
                    for target in drug.target_set.all():
                    
                        target.name = target.name.strip().upper()
                        if target.name in differential_genes[tumour]:
                            if int(db_choice) == 1:
                                pathways = Pathway.objects.filter(gene__name=target.name) # Human DB
                            elif int(db_choice) == 2:
                                pathways = MetabolismPathway.objects.filter(metabolismgene__name=target.name)# Metabolism DB
                            elif int(db_choice) == 3:
                                pathways = MousePathway.objects.filter(mousegene__name=target.name) # Mouse DB
                            
                    
                            for path in pathways:
                                try:
                                    
                                    if int(db_choice) == 1:
                                        gene = Gene.objects.get(name = target.name, pathway=path) # get Genes from Human DB
                                    elif int(db_choice) == 2:
                                        gene = MetabolismGene.objects.get(name = target.name, pathway=path) # get Genes from Metabolism DB
                                    elif int(db_choice) == 3:
                                        gene = MouseGene.objects.get(name = target.name, pathway=path) # get Genes from Mouse DB
                                    
                                except MultipleObjectsReturned:
                                    if int(db_choice) == 1:
                                        gene = Gene.objects.filter(name = target.name, pathway=path)[0] # get Genes from Human DB
                                    elif int(db_choice) == 2:
                                        gene = MetabolismGene.objects.filter(name = target.name, pathway=path)[0] # get Genes from Metabolism DB
                                    elif int(db_choice) == 3:
                                        gene = MouseGene.objects.filter(name = target.name, pathway=path)[0] # get Genes from Mouse DB
                                        
                                ARR = float(gene.arr)
                                CNR = process_doc_df.at[target.name, tumour]
                                if CNR == 0:
                                    CNR = 1
                                PMS = output_pas_df.at[path.name, tumour]
                                PMS2 = output_pas2_df.at[path.name, tumour]
                                AMCF = float(path.amcf)
                            
                                if drug.tip == 'inhibitor' and path.name!='Mab_targets':
                                    DS1 += PMS
                                    DS3 += PMS2
                                    DS2 += AMCF*ARR*math.log10(CNR)
                                if drug.tip == 'activator' and path.name!='Mab_targets':
                                    DS1 -= PMS
                                    DS3 -= PMS2
                                    DS2 -= AMCF*ARR*math.log10(CNR)
                                if drug.tip == 'mab' and path.name!='Mab_targets':
                                    DS1 += PMS
                                    DS3 += PMS2
                                    DS2 += AMCF*ARR*math.log10(CNR)
                                if drug.tip == 'mab' and path.name=='Mab_targets':
                                    DS1 += abs(PMS) # PMS2
                                    DS3 += abs(PMS2)
                                if drug.tip == 'killermab' and path.name=='Mab_targets':
                                    DS1 += abs(PMS)# PMS2
                                    DS3 += abs(PMS2)
                                    DS2 += math.log10(CNR)
                                if drug.tip == 'multivalent' and path.name!='Mab_targets':
                                    DS1 += PMS
                                    DS3 += PMS2
                                    if target.tip>0:
                                        DS2 -= AMCF*ARR*math.log10(CNR)
                                    else:
                                        DS2 += AMCF*ARR*math.log10(CNR)
                                    
                    ds1_dict[tumour] = DS1
                    ds2_dict[tumour] = DS2
                    ds3_dict[tumour] = DS3
            
                ds1_list.append(ds1_dict)
                ds2_list.append(ds2_dict)
                ds3_list.append(ds3_dict)
            
            output_ds1_df = DataFrame(ds1_list)
            output_ds1_df = output_ds1_df.set_index('Drug')
            output_ds2_df = DataFrame(ds2_list)
            output_ds2_df = output_ds2_df.set_index('Drug')
            output_ds3_df = DataFrame(ds3_list)
            output_ds3_df = output_ds3_df.set_index('Drug')
        
               
                    
        """ Saving results to Excel file and to database """
        path = os.path.join('users', str(input_document.project.owner),
                                            str(input_document.project),'output')
        file_name = 'output_'+str(input_document.get_filename()+'.xlsx')
        
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        
        output_file = default_storage.save(settings.MEDIA_ROOT+"/"+path+"/"+file_name, ContentFile(''))
               
        with ExcelWriter(output_file, index=False) as writer:
            if calculate_pas:
                output_pas_df.to_excel(writer,'PAS')
            if calculate_pas1:     
                output_pas1_df.to_excel(writer,'PAS1')
            if calculate_pas2:     
                output_pas2_df.to_excel(writer,'PAS2')
            if calculate_ds1:
                output_ds1_df.to_excel(writer, 'DS1A')
            if calculate_ds2:
                output_ds2_df.to_excel(writer, 'DS2')
            if calculate_ds3:
                output_ds3_df.to_excel(writer, 'DS1B')
        
        
        output_doc.document = path+"/"+os.path.basename(output_file)
        output_doc.related_doc = input_document
        output_doc.save() 
        
        """Create CNR file avaliable for downloading """
        
        cnr_norms_df = cnr_doc_df[[norm for norm in [col for col in cnr_doc_df.columns if 'Norm' in col]]]
        cnr_mean_norm =  cnr_norms_df.mean(axis=1)        
        cnr_gMean_norm = cnr_norms_df.apply(gmean, axis=1)
        std=cnr_norms_df.std(axis=1) # standard deviation
        if norm_choice>1: #geometric norms
            divide = cnr_gMean_norm
        else:             #arithmetic norms
            divide = cnr_mean_norm  
        
        cnr_doc_df = cnr_doc_df.div(divide, axis='index')
        
        cnr_doc_df['Mean_norm'] = cnr_mean_norm
        cnr_doc_df['gMean_norm'] = cnr_gMean_norm
        cnr_doc_df['std'] = std
        
        """ Saving CNR results to Excel file""" 
        path = os.path.join('users', str(input_document.project.owner),
                                            str(input_document.project),'process')
        file_name = 'cnr_'+str(output_doc.get_filename())
        
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        
        output_file = default_storage.save(settings.MEDIA_ROOT+"/"+path+"/"+file_name, ContentFile(''))
      
        with ExcelWriter(output_file, index=False) as writer:
            cnr_doc_df.to_excel(writer,'CNR')  
        
        
        
        
        return HttpResponseRedirect(reverse('document_detail', args=(output_doc.id,)))
    
        
    def form_invalid(self, form):
            return self.render_to_response(self.get_context_data(form=form))
        
class CoreCalculation(DetailView):
    model = ProcessDocument
    template_name = 'core/core_calculation.html'
    context_object_name = 'document'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CoreCalculation, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
              
        context = super(CoreCalculation, self).get_context_data(**kwargs)
        return context
    
class Test(TemplateView):
    """
    Just Testing Playground
    """
    template_name = 'core/test.html'
    
    
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(Test, self).dispatch(request, *args, **kwargs)
        
    
    def get_context_data(self, **kwargs):
              
        context = super(Test, self).get_context_data(**kwargs)
        from scipy.stats import ttest_1samp
    
        import numpy as np
        
        popmean = np.log(677.583249)
        a=np.array([212.226597,
           98.964291,
           210.267198,
           192.158336,
           250.711585,
           212.183150,
           226.327190,
           211.964368,
           217.831440,
           235.440940,
           245.281362,
           213.776852,
           195.193613])
        true_mean = sum(a) / float(len(a))
        a = np.log(a)
        from scipy.stats.mstats import gmean
        import scipy
        geom_Mean = gmean(a) 
        
        std = a.std()
        
        Zscore = (popmean-geom_Mean)/std
        
        
        
        p_values = scipy.stats.norm.pdf(Zscore)*2
                
        stat, pval = ttest_1samp(a, popmean)
        
        from .stats import pseudo_ttest_1samp  
        z_stat, p_val = pseudo_ttest_1samp(a, popmean)
           
        raise Exception('test exception')
        """
        from database.models import GOEnrichment
        for filename in os.listdir(settings.MEDIA_ROOT+"/GO/GO_enrichment"):
        
           
            try:
                spp = os.path.basename(filename).split('_', 2)
                pname=spp[2].split('.')[0]
                pathname = Pathway.objects.get(name=pname)
                ontology = spp[1]
            
            
                sniffer = csv.Sniffer()
                dialect = sniffer.sniff(open(settings.MEDIA_ROOT+"/GO/GO_enrichment/"+filename, 'r').read(), delimiters='\t,;') # defining the separator of the csv file
        
                input_doc_df = read_csv(settings.MEDIA_ROOT+"/GO/GO_enrichment/"+filename, delimiter=dialect.delimiter)
            
                for row_index, row in input_doc_df.iterrows():
                    newObj = GOEnrichment()
                    newObj.human_pathway = pathname
                    newObj.ontology = ontology
                
                    try:
                        newObj.GOID = row['GOBPID']
                    except:
                        try:
                            newObj.GOID = row['GOMFID']
                        except:
                            newObj.GOID = row['GOCCID']
                        
                    newObj.Pvalue = float(row['Pvalue'])
                    newObj.OddsRatio = row['OddsRatio']
                    newObj.ExpCount = float(row['ExpCount'])
                    newObj.Count = int(row['Count'])
                    newObj.Size = int(row['Size'])
                    newObj.Term = row['Term']
                
                    newObj.save()
            except:
                raise
                
            
            
            
            
           
        
            
             
        
        
        
        
        
        path = Pathway.objects.using('old').get(name="Wnt_Pathway_Ctnn-b_Degradation")
        
        path1 = Pathway.objects.using('old').get(name="Wnt_Pathway_Ctnn-b_Degradation")
        
        
        path.save(using="default")
        
        for gene in path1.gene_set.all():
            gene.save(using="default")
            
        for node in path1.node_set.all():
            node.save(using="default")
            
        for node in path1.node_set.all():
            for component in node.component_set.all():
                component.save(using="default")
                
        for node in path1.node_set.all():
            for inrel in node.inrelations.all():
                inrel.save(using="default")
            
        
        
        """
        
        
        
        
        return context


class Celery(TemplateView):
    """
    Testing Celery tasks
    """
    template_name = 'core/celery.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(Celery, self).dispatch(request, *args, **kwargs)
    
    
    def get_context_data(self, **kwargs):
              
        context = super(Celery, self).get_context_data(**kwargs)
        
        return context
    
        
class TaskStatus(TemplateView):
    """ Testing Celery task status via Ajax"""
    
    template_name = 'core/test.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        
        if self.request.is_ajax():
            import json
            from django.http import HttpResponse
            from celery.result import AsyncResult
            
            task_id = self.request.POST.get('task_id')
            task = AsyncResult(task_id)
            state = task.state
            result = task.result if task.result else 'not done'
            
            data = {'state': state,
                    'result': result}
            
            
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
        
            return super(TaskStatus, self).dispatch(request, *args, **kwargs)
    
    
    def get_context_data(self, **kwargs):
              
        context = super(TaskStatus, self).get_context_data(**kwargs)
        
        return context
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
