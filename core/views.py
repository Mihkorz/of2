# -*- coding: utf-8 -*-
import os
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
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from .forms import  CalculationParametersForm, MedicCalculationParametersForm
from profiles.models import Document, ProcessDocument
from .models import Pathway, Gene, Node, Component, Relation
from database.models import Drug, Target
from metabolism.models import MetabolismPathway, MetabolismGene
from mouse.models import MousePathway, MouseGene, MouseMetabolismPathway, MouseMetabolismGene, MouseMapping
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
        use_new_fdr = form.cleaned_data.get('use_new_fdr', True)
        use_ttest_stat = form.cleaned_data.get('use_ttest_stat', True) #for OF_cnr_stat files
        use_fdr_stat = form.cleaned_data.get('use_fdr_stat', False) #for OF_cnr_stat files
        use_ttest_1sam = form.cleaned_data.get('use_ttest_1sam', False) 
        pvalue_threshold = form.cleaned_data.get('pvalue_threshold', 0.05)
        qvalue_threshold = form.cleaned_data.get('qvalue_threshold', 0.05)        
        use_cnr = form.cleaned_data.get('use_cnr', True)
        cnr_low = form.cleaned_data.get('cnr_low', 0.67)
        cnr_up =  form.cleaned_data.get('cnr_up', 1.5)
        use_sigma = form.cleaned_data.get('use_sigma', False) # !!! deprecated !!! 
        sigma_num = form.cleaned_data.get('sigma_num', 2) # !!! deprecated !!!
        
        #database and normal choice
        organism_choice = form.cleaned_data.get('organism_choice', 'human') #default=human
        db_choice = form.cleaned_data.get('db_choice', ['primary_old']) #default=primary_old
        db_choice_drug = form.cleaned_data.get('db_choice_drug', ['oncofinder']) #default=oncofinder
        norm_choice = form.cleaned_data.get('norm_choice', 2) #default=geometric 
        
        #what to calculate and include in output report
        calculate_pas = form.cleaned_data.get('calculate_pas', False)
        calculate_pas1 = form.cleaned_data.get('calculate_pas1', True)
        calculate_pas2 = form.cleaned_data.get('calculate_pas2', False)
        calculate_ds1a = form.cleaned_data.get('calculate_ds1a', False)
        calculate_ds2 = form.cleaned_data.get('calculate_ds2', False)
        calculate_ds1b = form.cleaned_data.get('calculate_ds1b', False)
        calculate_norms_pas = form.cleaned_data.get('calculate_norms_pas', False)
        calculate_pvalue_each = form.cleaned_data.get('calculate_pvalue_each', False)
        calculate_pvalue_all = form.cleaned_data.get('calculate_pvalue_all', False)
        calculate_FDR_each = form.cleaned_data.get('calculate_FDR_each', False)
        calculate_FDR_all = form.cleaned_data.get('calculate_FDR_all', False)  
        new_pathway_names = form.cleaned_data.get('new_pathway_names', False)
        diff_genes_amount = form.cleaned_data.get('diff_genes_amount', False)
        
        
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
        
        output_doc.parameters = {'sigma_num': sigma_num,
                                 'use_sigma': use_sigma,
                                 'cnr_low': cnr_low,
                                 'cnr_up': cnr_up,
                                 'use_cnr': use_cnr,
                                 'use_ttest': use_ttest,
                                 'use_fdr': use_fdr,
                                 'use_new_fdr': use_new_fdr,
                                 'use_ttest_1sam': use_ttest_1sam,
                                 'norm_algirothm': 'geometric' if int(norm_choice)>1 else 'arithmetic',
                                 'organism': organism_choice, 
                                 'db': db_choice,
                                 'hormone_status': hormone_status,
                                 'her2_status': her2_status }
        
        output_doc.project = input_document.project
        output_doc.created_by = self.request.user
        output_doc.created_at = datetime.now()        
        #output_doc.save()
        
        params_for_output = []
        params_for_output.append({'Parameters': 'Organism: '+organism_choice})
        params_for_output.append({'Parameters': 'Database(s): '+', '.join(db_choice) })
        params_for_output.append({'Parameters': 'Calculation algorithm for normal values: '+ ('geometric' if int(norm_choice)>1 else 'arithmetic') })
        
        params_for_output.append({'Parameters': 'Used T-test for gene distribution: '+ ('Yes' if use_ttest else 'No') })
        params_for_output.append({'Parameters': 'Used 1sample T-test: '+ ('Yes' if use_ttest_1sam else 'No') })
        params_for_output.append({'Parameters': 'Used FDR for T-test: '+ ('Yes' if use_fdr else 'No') })
        params_for_output.append({'Parameters': 'Used CNR filter: '+ ('Yes. Lower limit='+str(cnr_low)+'. Upper limit='+str(cnr_up) if use_cnr else 'No') })
        params_for_output.append({'Parameters': 'Used Sigma filer: '+ ('Yes. Sigma number='+str(sigma_num) if use_sigma else 'No') })
        
        params_df = DataFrame(params_for_output)
                
        """ Start Calculations"""
        print 'start calc'
        def strip(text):
            try:
                return text.strip().upper()
            except AttributeError:
                return text
        
        calculate_p_value = False # Flag for p-value calculation
        
        process_doc_df = read_csv(settings.MEDIA_ROOT+"/"+input_document.input_doc.document.name,
                                  sep='\t', index_col='SYMBOL',  converters = {'SYMBOL' : strip}).fillna(0)        
        
        process_doc_df = process_doc_df.groupby(process_doc_df.index,
                                                level=0).mean() #deal with duplicate genes by taking mean value
        
        # DataBase choice
          
        pathway_objects = Pathway.objects.filter(organism=organism_choice,
                                                 database__in=db_choice
                                                 ).prefetch_related('gene_set')
        
        all_genes = DataFrame(list(Gene.objects.filter(pathway__database__in=db_choice).values_list('name', flat=True).distinct())).set_index(0)#fetch genes    
        all_genes.index.name = 'SYMBOL'
        
        
        process_doc_df = all_genes.join(process_doc_df, how='inner') # leave only genes that are in our DB
        tumour_columns = [col for col in process_doc_df.columns if 'Tumour' in col] #get sample columns 
        normal_columns = [col for col in process_doc_df.columns if 'Norm' in col] #get normal columns
        
        
        cnr_doc_df =  process_doc_df.copy() # use to generate CNR file for downloading
        if input_document.doc_format!='OF_cnr' and input_document.doc_format!='OF_cnr_stat':
            cnr_norms_df = cnr_doc_df[normal_columns]
            std=cnr_norms_df.std(axis=1) # standard deviation
            if int(norm_choice)>1: #geometric norms
                cnr_gMean_norm = cnr_norms_df.apply(gmean, axis=1).fillna(1)
                #cnr_gMean_norm = cnr_gMean_norm.astype(np.float).fillna(1)
                cnr_doc_df = cnr_doc_df.div(cnr_gMean_norm, axis='index')
                cnr_doc_df['gMean_norm'] = cnr_gMean_norm
                process_doc_df['mean'] = cnr_gMean_norm
            else:             #arithmetic norms
                cnr_mean_norm =  cnr_norms_df.mean(axis=1)
                cnr_doc_df = cnr_doc_df.div(cnr_mean_norm, axis='index') 
                cnr_doc_df['Mean_norm'] = cnr_mean_norm
                process_doc_df['mean'] = cnr_mean_norm           
            
            cnr_doc_df['std'] = std
        
        
        
        cnr_unchanged_df = cnr_doc_df.copy()
        
        """ Standard T-test for genes """
        if use_ttest:
            
            def calculate_ttest(row):
                tumours = row[tumour_columns]
                norms = row[normal_columns]
                 
                _, p_val = ttest_ind(tumours, norms)
                
                return p_val
            log_process_doc_df = np.log(process_doc_df.astype('float32')).fillna(0)
            series_p_values = log_process_doc_df.apply(calculate_ttest, axis=1).fillna(1)
            log_process_doc_df = None
            
            process_doc_df['p_value'] = series_p_values
            cnr_doc_df['p_value'] = series_p_values
            #raise Exception('stop')
            if use_fdr or use_new_fdr:
                if use_new_fdr:
                    fdr_q_values = fdr_corr(np.array(series_p_values), pi0=-1)
                else:
                    fdr_q_values = fdr_corr(np.array(series_p_values))
                fdr_df = DataFrame({'p' : series_p_values,
                                    'q' : fdr_q_values
                                    })
                process_doc_df['q_value'] = fdr_df['q']
                cnr_doc_df['q_value'] = fdr_df['q']
                cnr_doc_df[fdr_df['q']>=qvalue_threshold] = 1
                process_doc_df = process_doc_df[fdr_df['q']<qvalue_threshold]
                
            else:
                cnr_doc_df[process_doc_df['p_value']>=pvalue_threshold] = 1
                process_doc_df = process_doc_df[process_doc_df['p_value']<pvalue_threshold]
            
            
        print 't-test done'         
        """ T-test 1 sample CNR filter and Sigma filter for genes """
        if use_ttest_1sam or use_cnr or use_sigma:
            norms_df = process_doc_df[normal_columns]
            log_norms_df = np.log(norms_df)#use this for t-test, assuming log(norm) is distributed normally
            
            df_for_pq_val = DataFrame()
            def filter_diff_genes(col):
                if ('Tumour' in col.name) or ('Norm' in col.name):
                    if input_document.doc_format!='OF_cnr' and input_document.doc_format!='OF_cnr_stat':
                        col_CNR = col/process_doc_df['mean'] #convert column from GENE EXPRESSION to CNR
                    else:
                        col_CNR = col
                    if use_ttest_1sam: # two-sided 1sample T-test filter
                        _, p_value = ttest_1samp(log_norms_df, np.log(col), axis=1)
                        s_p_value = Series(p_value, index = col.index).fillna(1)
                        df_for_pq_val[col.name+'_pval'] = s_p_value
                        if use_fdr or use_new_fdr:
                            if use_new_fdr:
                                fdr_q_values = fdr_corr(np.array(s_p_value),  pi0=-1)
                            else:
                                fdr_q_values = fdr_corr(np.array(s_p_value))
                                
                            df_for_pq_val[col.name+'_qval'] = fdr_q_values
                            col_CNR[fdr_q_values>=qvalue_threshold] = 1
                        else:
                            col_CNR[s_p_value>=pvalue_threshold] = 1               
                        
                                      
                    if use_cnr: # CNR FILTER
                        col_CNR[((col_CNR<=cnr_up) & (col_CNR>=cnr_low))] = 1 
                        
                    if use_sigma: # Sigma FILTER  !!! deprecated !!!
                        
                        cnr_std = cnr_doc_df['std']
                        std = cnr_std[cnr_std!=1]
                                                 
                        col_CNR[((col<(process_doc_df['mean']+sigma_num*std)) &
                                       (col>=(process_doc_df['mean']-sigma_num*std)))] = 1 
                    
                    return col_CNR
                       
                else:
                    return col # in case it's not Tumour or Norm column
                     
            
            process_doc_df = process_doc_df.apply(filter_diff_genes, axis=0)
            
            cnr_df_diff_genes = process_doc_df.copy() 
            if input_document.doc_format!='OF_cnr' and input_document.doc_format!='OF_cnr_stat':
                oldstd = cnr_doc_df['std']
                old_meanNorm = cnr_doc_df['gMean_norm']
                cnr_doc_df = cnr_df_diff_genes.join(df_for_pq_val)
                cnr_doc_df['std'] = oldstd
                cnr_doc_df['gMean_norm'] = old_meanNorm
            #raise Exception('test cnr')
            cnr_doc_df.fillna(1, inplace=True)
            cnr_doc_df = cnr_doc_df.sort_index(axis=1)        
        else:
            if input_document.doc_format!='OF_cnr' and input_document.doc_format!='OF_cnr_stat':
                process_doc_df = process_doc_df.div(process_doc_df['mean'], axis='index') #convert column from GENE EXPRESSION to CNR
        
        if input_document.doc_format=='OF_cnr_stat': #for OF_cnr_stat files only
            def filter_from_file_stat(col):
                if 'Tumour' in col.name:
                    sample_name = col.name.replace("Tumour", "")
                    p_val_col = "ttest_pv"+sample_name
                    q_val_col = "ttest_fdr"+sample_name
                    if use_ttest_stat:
                        col = col[(process_doc_df[p_val_col]<0.05)]
                    if use_fdr_stat:
                        col = col[(process_doc_df[q_val_col]<0.05)]
                    
                    return col
                else:
                    return col    
                
            process_doc_df = process_doc_df.apply(filter_from_file_stat, axis=0,).fillna(1)
            
            
        """ end of calculating horizontal p-values for genes """
        
        if input_document.norm_num >= 3:
            calculate_p_value = True                                
        
        """ Inserting new pathway names if needed """
        if new_pathway_names:
            if 'primary_old' in db_choice:
                new_path_primary_old = read_excel(settings.MEDIA_ROOT+"/TRpathways_update_final_updated2.xlsx",
                                         sheetname=0,
                                         index_col='Old Pathway Name')
            if 'primary_new' in db_choice:
                new_path_primary_new = read_excel(settings.MEDIA_ROOT+"/primary_new_pathways_renaming.xlsx",
                                         sheetname=0, 
                                         index_col='Old Pathway Name')
            if 'cytoskeleton' in db_choice:
                new_path_cytoskeleton = read_excel(settings.MEDIA_ROOT+"/cytoskeleton_new_pathways_renamed.xlsx",
                                         sheetname=0, 
                                         index_col='Old Pathway Name')
            
        
        #raise Exception('before cycle')
        """ START CYCLE """
        output_pas_df  = DataFrame()
        output_pas1_df = DataFrame()
        output_pas2_df = DataFrame()
        
        output_dg_amount = DataFrame() #count differential genes amount and ratio
        output_dg_ratio = DataFrame()  #for Nicolay special 
        
        i=0
        for pathway in pathway_objects:
            
            gene_objects = pathway.gene_set.all()
              
            gene_data = []
            for gene in gene_objects:
                gene_data.append({'SYMBOL':gene.name.strip().upper(),
                                  'ARR':float(gene.arr) })   
           
            gene_df = DataFrame(gene_data).set_index('SYMBOL')
            
            if diff_genes_amount:
                gene_number = len(gene_df.index) 
               
            gene_df_abs = gene_df.abs() #for PAS2 calculation
            summ_genes_arr = (gene_df_abs['ARR'].sum() 
                              if gene_df_abs['ARR'].sum()>0 else 1) #for PAS2 calculation
            
            gene_df = gene_df.groupby(gene_df.index, level=0).mean() # take average value for duplicate genes 
            
            joined_df = gene_df.join(process_doc_df, how='inner') #intersect DataFrames to acquire only genes in current pathway
            
            """ Calculating PAS1 for samples and norms """
            pas1_norms_samples = np.log(joined_df[tumour_columns+normal_columns].astype('float32'))
            pas1_norms_samples = pas1_norms_samples.multiply(joined_df['ARR'], axis='index')
            
            pas1_norms_samples = pas1_norms_samples.sum() # now we have PAS1                      
            pas_norms_samples = pas1_norms_samples*float(pathway.amcf) # PAS
            pas2_norms_samples = pas1_norms_samples/summ_genes_arr # PAS2
            
            if calculate_p_value and (calculate_pvalue_each or calculate_pvalue_all):
                s_norms_pas = pas_norms_samples[normal_columns]
                s_samples_pas = pas_norms_samples[tumour_columns]
                
                s_norms_pas1 = pas1_norms_samples[normal_columns]
                s_samples_pas1 = pas1_norms_samples[tumour_columns]
                
                s_norms_pas2 = pas2_norms_samples[normal_columns]
                s_samples_pas2 = pas2_norms_samples[tumour_columns]   
                
            """P-value for each sample(parametric test)"""
            if calculate_p_value and calculate_pvalue_each: 
                            
                tt_norm_pas  = DataFrame(index=tumour_columns, columns=normal_columns )
                tt_norm_pas1 = DataFrame(index=tumour_columns, columns=normal_columns )
                tt_norm_pas2 = DataFrame(index=tumour_columns, columns=normal_columns )
                
                for norm_name in normal_columns:
                    tt_norm_pas[norm_name] = s_norms_pas[norm_name]
                    tt_norm_pas1[norm_name] = s_norms_pas1[norm_name]
                    tt_norm_pas2[norm_name] = s_norms_pas2[norm_name]
                
                #_, p_val = pseudo_ttest_1samp(tt_norm_pas, s_samples_pas, axis=1)
                _, p_val = ttest_1samp(tt_norm_pas, s_samples_pas, axis=1)
                s_p_value = Series(p_val, index = s_samples_pas.index+'_p-val').fillna(1)
                pas_norms_samples = pas_norms_samples.append(s_p_value) 
                
                #_, p_val = pseudo_ttest_1samp(tt_norm_pas1, s_samples_pas1, axis=1)
                _, p_val = ttest_1samp(tt_norm_pas1, s_samples_pas1, axis=1)
                s_p_value = Series(p_val, index = s_samples_pas1.index+'_p-val').fillna(1)
                pas1_norms_samples = pas1_norms_samples.append(s_p_value)
                
                #_, p_val = pseudo_ttest_1samp(tt_norm_pas2, s_samples_pas2, axis=1)
                _, p_val = ttest_1samp(tt_norm_pas2, s_samples_pas2, axis=1)
                s_p_value = Series(p_val, index = s_samples_pas2.index+'_p-val').fillna(1)
                pas2_norms_samples = pas2_norms_samples.append(s_p_value)               
                
            """P-value for each pathway(non-parametric test)"""
            if calculate_p_value and calculate_pvalue_all:
                
                _, p_val = ranksums(s_norms_pas, s_samples_pas)
                pas_norms_samples['p-value_Mean'] = p_val
                
                _, p_val = ranksums(s_norms_pas1, s_samples_pas1)
                pas1_norms_samples['p-value_Mean'] = p_val
                
                _, p_val = ranksums(s_norms_pas2, s_samples_pas2)
                pas2_norms_samples['p-value_Mean'] = p_val 
            
            """Calculate differential genes amount and ratio for Nicolay"""
            if diff_genes_amount:
                
                dif_genes_df = joined_df[tumour_columns]
                def count_diff_genes(col):
                    col = col[col!=1]
                    return col.count()
                
                count_genes = dif_genes_df.apply(count_diff_genes)
                count_genes_ratio = count_genes.divide(gene_number)
                count_genes_ratio=count_genes_ratio.round(2)
                count_genes['Pathway']=count_genes_ratio['Pathway']=pathway.name
                count_genes['Database']=count_genes_ratio['Database']=pathway.database
                
                output_dg_amount[i] = count_genes
                output_dg_ratio[i] = count_genes_ratio
                
            
            pas_norms_samples['Pathway'] = pas1_norms_samples['Pathway']=pas2_norms_samples['Pathway']= pathway.name
            pas_norms_samples['Database'] = pas1_norms_samples['Database']=pas2_norms_samples['Database']= pathway.database
            
            
            if new_pathway_names:
                new_name = pathway.name
                try:
                    if pathway.database == 'primary_old':
                        new_name = new_path_primary_old.loc[pathway.name]['Pathway Name']
                    if pathway.database == 'primary_new':
                        new_name = new_path_primary_new.loc[pathway.name]['Pathway Name']
                    if pathway.database == 'cytoskeleton':
                        new_name = new_path_cytoskeleton.loc[pathway.name]['Pathway Name']
                except:
                    new_name = pathway.name
               
                pas_norms_samples['New Pathway name'] = pas1_norms_samples['New Pathway name']=pas2_norms_samples['New Pathway name']= new_name     
                    
                
            
            
            output_pas_df[i]= pas_norms_samples
            output_pas1_df[i]= pas1_norms_samples
            output_pas2_df[i]= pas2_norms_samples

            i=i+1
        """ END CYCLE """
        
        
        """ Creating output DataFrames """
        output_pas_df = output_pas_df.T
        output_pas_df.set_index('Pathway', inplace=True)
        
        output_pas1_df = output_pas1_df.T
        output_pas1_df.set_index('Pathway', inplace=True)
        
        output_pas2_df = output_pas2_df.T
        output_pas2_df.set_index('Pathway', inplace=True)
        
        if diff_genes_amount:
            output_dg_amount = output_dg_amount.T
            output_dg_amount.set_index('Pathway', inplace=True)
            output_dg_ratio = output_dg_ratio.T
            output_dg_ratio.set_index('Pathway', inplace=True)
            
            output_dg_amount.sort(axis=1, inplace=True)
            output_dg_ratio.sort(axis=1, inplace=True)
           
            
           
        if calculate_FDR_all:
                output_pas1_df['q-value_Mean'] = fdr_corr(np.array(output_pas1_df['p-value_Mean']))
        if calculate_FDR_each:
                col_p_val = [col for col in output_pas1_df.columns if '_p-value' in col]
                for col in col_p_val:
                    q_val_column_name = col.replace("_p-value", "_q-value");
                    output_pas1_df[col].fillna(1, inplace=True)
                    output_pas1_df[q_val_column_name] = fdr_corr(np.array(output_pas1_df[col]))
        
        
        """ Inserting new pathway names if needed 
        if new_pathway_names:
            if pathway.database == 'primary_new':
                new_path_df = read_excel(settings.MEDIA_ROOT+"/primary_new_pathways_renaming.xlsx",
                                         sheetname=0, 
                                         index_col='Old Pathway Name')
            else:                    
                new_path_df = read_excel(settings.MEDIA_ROOT+"/TRpathways_update_final_updated2.xlsx",
                                         sheetname=0,
                                         index_col='Old Pathway Name')
            new_path_names=new_path_df['Pathway Name']
                       
            output_pas_df = output_pas_df.join(new_path_names)
            idx = output_pas_df['Pathway Name'].isnull( )
            output_pas_df['Pathway Name'][ idx ] = output_pas_df.index[ idx ]
            
            output_pas1_df = output_pas1_df.join(new_path_names)
            idx = output_pas1_df['Pathway Name'].isnull( )
            output_pas1_df['Pathway Name'][ idx ] = output_pas1_df.index[ idx ]
            
            output_pas2_df = output_pas2_df.join(new_path_names)
            idx = output_pas2_df['Pathway Name'].isnull( )
            output_pas2_df['Pathway Name'][ idx ] = output_pas2_df.index[ idx ]
        """
        
        if not calculate_norms_pas: #exclude norms from DF if checkbox is not selected
                output_pas_df.drop(normal_columns, axis=1, inplace=True)
                output_pas1_df.drop(normal_columns, axis=1,  inplace=True)
                output_pas2_df.drop(normal_columns,  axis=1, inplace=True)
                
        """ Sort paths Dataframes """
        output_pas_df.sort(axis=1, inplace=True)
        output_pas1_df.sort(axis=1, inplace=True)
        output_pas2_df.sort(axis=1, inplace=True)
        
        print 'PAS done'
        
        #raise Exception('fast PAS') 
        """ ###################  """
        """ new DS calculations  """
        """ ###################  """
        if (calculate_ds1a or calculate_ds2 or calculate_ds1b):
            
            output_ds1a_df = DataFrame()
            output_ds1b_df = DataFrame()
            output_ds2_df = DataFrame()
            
            """ Select Drugs Databese """
            drugs_db = []
            for db in db_choice_drug:
                if db == 'geroscope':
                    append_db = ['drugbank_geroscope', 'primary_geroscope']
                else:
                    append_db = ['drugbank', 'primary']
                drugs_db = drugs_db+append_db
            
            """ Create Series [target.name] - [pathways it's involved in] """
            targets = Target.objects.values_list('name', flat=True).distinct()
            s_target_path = Series()
            for target in targets:
                paths = Pathway.objects.filter(gene__name=target, organism=organism_choice,
                                                 database__in=db_choice).values_list('name', 'amcf', 'gene__arr')
                
                s_target_path =  s_target_path.set_value(target, paths)
                
                       
            drug_objects = Drug.objects.filter(db__in=drugs_db).prefetch_related('target_set')
            d=0
            for drug in drug_objects:
                #print drug.name

                ds1a_df = DataFrame(index=tumour_columns)
                ds1b_df = DataFrame(index=tumour_columns)
                ds2_df  = DataFrame(index=tumour_columns)
                
                t=0
                for target in drug.target_set.all():
                    for path_details in s_target_path[target.name]: #path_details=(pathway.name, pathway.amcf, gene.arr)
                        
                        path_name = path_details[0]
                        amcf = float(path_details[1])
                        arr = float(path_details[2])
                        
                        ds1a_s = output_pas_df.loc[path_details[0]][tumour_columns]
                        ds1a_df[str(t)+'_'+path_name] = ds1a_s
                        
                        ds1b_s = output_pas2_df.loc[path_details[0]][tumour_columns]
                        ds1b_df[str(t)+'_'+path_name] = ds1b_s*amcf
                        
                        try:
                            cnr_s = process_doc_df.loc[target.name][tumour_columns]
                        except:
                            cnr_s = 1
                        if drug.tip == 'multivalent' and target.tip>0:
                            m = -1
                        else:
                            m = 1
                        ds2_df[str(t)+'_'+path_name] = m*np.log10(cnr_s)*amcf*arr
                        
                        t=t+1                  
                        
                full_ds1a_s = ds1a_df.sum(axis=1)
                full_ds1b_s = ds1b_df.sum(axis=1)
                full_ds2_s = ds2_df.sum(axis=1)
                
                if drug.tip =='activator':
                    full_ds1a_s = -1*full_ds1a_s
                    full_ds1b_s = -1*full_ds1b_s
                    full_ds2_s = -1*full_ds2_s
                full_ds1a_s['Drug'] = full_ds1b_s['Drug'] = full_ds2_s['Drug'] =drug.name
                full_ds1a_s['Database'] = full_ds1b_s['Database'] = full_ds2_s['Database'] = drug.db
                full_ds1a_s['Drug type'] = full_ds1b_s['Drug type'] = full_ds2_s['Drug type'] = drug.tip                
                               
                
                output_ds1a_df[d] = full_ds1a_s
                output_ds1b_df[d] = full_ds1b_s
                output_ds2_df[d] = full_ds2_s     
                d=d+1
                #raise Exception(drug.name)        
                       
                    
            """ Creating output DataFrames """
            output_ds1a_df = output_ds1a_df.T
            output_ds1a_df.fillna(0, inplace=True)
            output_ds1a_df.set_index('Drug', inplace=True)
        
            output_ds1b_df = output_ds1b_df.T
            output_ds1b_df.fillna(0, inplace=True)
            output_ds1b_df.set_index('Drug', inplace=True)
        
            output_ds2_df = output_ds2_df.T
            output_ds2_df.fillna(0, inplace=True)
            output_ds2_df.set_index('Drug', inplace=True)
        
            """ Sort paths Dataframes """
            output_ds1a_df.sort(axis=1, inplace=True)
            output_ds1b_df.sort(axis=1, inplace=True)
            output_ds2_df.sort(axis=1, inplace=True)                
        
        
        """ Genegate Patient Report """
        if (calculate_ds1b and calculate_ds2 and len(tumour_columns)==1 ):
             
            patient_df = DataFrame(index=output_ds2_df.index)

            patient_df[u'№'] = ""
            patient_df[u'БД'] = output_ds2_df['Database']
            patient_df[u'Тип'] = output_ds2_df['Drug type']
            patient_df['DS2'] = output_ds2_df[tumour_columns]
            patient_df['DS1'] = output_ds1b_df[tumour_columns]        
        
            patient_df.index.name = u'Препарат'
            patient_df.reset_index(inplace=True)
            
            patient_df = patient_df.assign(total=((patient_df['DS1'] + patient_df['DS2'])/2))
            patient_df.sort('total', inplace=True, ascending=False)
        
            patient_df = patient_df[[u'№', u'Препарат', u'БД', 'DS1', 'DS2', u'Тип']]
            patient_df.reset_index(drop=True, inplace=True)
            
            primary_drugs_df = patient_df[patient_df[u'БД']=='primary']        
            primary_drugs_series = primary_drugs_df[u'Препарат']
        
        
                      
         
        """ OLD Calculating Drug Score 
        
        output_ds1_df = output_ds2_df = output_ds3_df = DataFrame()
        
        if (calculate_ds1 or calculate_ds2 or calculate_ds3):
            ds1_list = []
            ds2_list = []
            ds3_list = []
        
            for drug in Drug.objects.all(): #iterate trough all Drugs
                print drug.name
                ds1_dict = {}
                ds2_dict = {}
                ds3_dict = {}
                ds1_dict['Drug'] = ds2_dict['Drug'] = ds3_dict['Drug'] = drug.name.strip()
                ds1_dict['DataBase'] = ds2_dict['DataBase'] = ds3_dict['DataBase'] = drug.db
                ds1_dict['Type'] = ds2_dict['Type'] = ds3_dict['Type'] = drug.tip          
            
                ddd = []
                for tumour in tumour_columns: #loop thought samples columns
                    #print "TUMOUR: " + tumour
                    
                    DS1 = 0 # DrugScore 1
                    DS2 = 0 # DrugScore 2
                    DS3 = 0
                    
                                    
            
                    for target in drug.target_set.all():
                        
                        target.name = target.name.strip().upper()
                        if target.name in process_doc_df.index.values:#differential_genes[tumour]:
                            
                            pathways = Pathway.objects.filter(organism=organism_choice,
                                                 database__in=db_choice, gene__name=target.name)
                            
                            for path in pathways:
                                
                                gene = Gene.objects.filter(name = target.name, pathway=path)[0]
       
                                ARR = float(gene.arr)
                                CNR = process_doc_df.at[target.name, tumour]
                                if CNR == 0:
                                    CNR = 1
                                PMS = output_pas_df.at[path.name, tumour]
                                PMS2 = output_pas2_df.at[path.name, tumour]
                                AMCF = float(path.amcf)
                            
                                if drug.tip == 'inhibitor' and path.name!='Mab_targets':
                                    DS1 += PMS
                                    if tumour == 'Tumour_X5500024052861011409506.H02.CEL':
                                        ddd.append({path.name:PMS})
                                    DS3 += AMCF*PMS2
                                    DS2 += AMCF*ARR*math.log10(CNR)
                                if drug.tip == 'activator' and path.name!='Mab_targets':
                                    DS1 -= PMS
                                    DS3 -= AMCF*PMS2
                                    DS2 -= AMCF*ARR*math.log10(CNR)
                                if drug.tip == 'mab' and path.name!='Mab_targets':
                                    DS1 += PMS
                                    DS3 += AMCF*PMS2
                                    DS2 += AMCF*ARR*math.log10(CNR)
                                if drug.tip == 'mab' and path.name=='Mab_targets':
                                    DS1 += abs(PMS) # PMS2
                                    DS3 += abs(PMS2)
                                if drug.tip == 'killermab' and path.name=='Mab_targets':
                                    DS1 += abs(PMS)# PMS2
                                    DS3 += AMCF*abs(PMS2)
                                    DS2 += math.log10(CNR)
                                if drug.tip == 'multivalent' and path.name!='Mab_targets':
                                    DS1 += PMS
                                    DS3 += AMCF*PMS2
                                    if target.tip>0:
                                        DS2 -= AMCF*ARR*math.log10(CNR)
                                    else:
                                        DS2 += AMCF*ARR*math.log10(CNR)
                                
                                    
                    ds1_dict[tumour] = DS1
                    ds2_dict[tumour] = DS2
                    ds3_dict[tumour] = DS3
                raise Exception('drug = '+drug.name+' summ DS111A='+str(sum(ddd)))
                ds1_list.append(ds1_dict)
                ds2_list.append(ds2_dict)
                ds3_list.append(ds3_dict)
            raise Exception('exppp')
            #raise Exception('DS no drug')
            output_ds1_df = DataFrame(ds1_list)
            output_ds1_df = output_ds1_df.set_index('Drug')
            output_ds2_df = DataFrame(ds2_list)
            output_ds2_df = output_ds2_df.set_index('Drug')
            output_ds3_df = DataFrame(ds3_list)
            output_ds3_df = output_ds3_df.set_index('Drug')
        
        """       
                    
        """ Saving results to Excel file and to database """
        path = os.path.join('users', str(input_document.project.owner),
                                            str(input_document.project),'output')
        file_name = 'output_'+str(input_document.get_filename()+'.xlsx')
        
        
        output_file = default_storage.save(settings.MEDIA_ROOT+"/"+path+"/"+file_name, ContentFile(''))
        
              
        with ExcelWriter(output_file, engine='xlsxwriter' ) as writer:
            if calculate_pas:
                output_pas_df.sort('Database', inplace=True)
                output_pas_df.reset_index(inplace=True)
                output_pas_df.to_excel(writer,'PAS', index=False)
            if calculate_pas1:
                output_pas1_df.sort('Database', inplace=True)
                output_pas1_df.reset_index(inplace=True)     
                output_pas1_df.to_excel(writer,'PAS1', index=False)
            if calculate_pas2:
                output_pas2_df.sort('Database', inplace=True)
                output_pas2_df.reset_index(inplace=True)     
                output_pas2_df.to_excel(writer,'PAS2', index=False)
            if calculate_ds1a:
                output_ds1a_df.reset_index(inplace=True)
                output_ds1a_df.to_excel(writer, 'DS1A', index=False)
            if calculate_ds2:
                output_ds2_df.reset_index(inplace=True)
                output_ds2_df.to_excel(writer, 'DS2', index=False)
            if calculate_ds1b:
                output_ds1b_df.reset_index(inplace=True)
                output_ds1b_df.to_excel(writer, 'DS1B', index=False)
            
            if (calculate_ds1b and calculate_ds2 and len(tumour_columns)==1 ):
                patient_df.to_excel(writer, 'Patient report', index=False)
                
                workbook = writer.book
                worksheet = writer.sheets['Patient report']
        
                num_fmt = workbook.add_format({'align': 'right', 'num_format': '0.0', 'border':True})
                bold_fmt = workbook.add_format({'align': 'left', 'bold':True, 'border':True})
                border_fmt = workbook.add_format({'border':True})
        
                color_fmt = workbook.add_format({'bg_color': '#CCCCCC'})
        
                worksheet.set_column('A:A', 5, border_fmt)
                worksheet.set_column('B:B', 30, bold_fmt)       
                worksheet.set_column('C:C', 10, border_fmt)
                worksheet.set_column('D:E', 10, border_fmt)
                worksheet.set_column('D:E', 10, num_fmt)
                worksheet.set_column('F:F', 10, border_fmt)
        
                for index,value in primary_drugs_series.iteritems():
                    worksheet.write('B'+str(index+2), value, color_fmt)
            
            
            if diff_genes_amount:
                output_dg_amount.sort('Database', inplace=True)
                output_dg_amount.reset_index(inplace=True)     
                output_dg_amount.to_excel(writer,'Diff genes amount', index=False)                
                output_dg_ratio.sort('Database', inplace=True)
                output_dg_ratio.reset_index(inplace=True)     
                output_dg_ratio.to_excel(writer,'Diff genes ratio', index=False)
                
            params_df.to_excel(writer,'Parameters')
        
        output_doc.document = path+"/"+os.path.basename(output_file)
        output_doc.related_doc = input_document
        output_doc.save() 
        
        """Create CNR file available for downloading """
        
        """ Saving CNR results to Excel file """
        path = os.path.join('users', str(input_document.project.owner),
                                            str(input_document.project),'process')
        file_name = 'cnr_'+str(output_doc.get_filename())
        file_name_unchanged = 'cnr_row_'+str(output_doc.get_filename()) 
        
        output_file = default_storage.save(settings.MEDIA_ROOT+"/"+path+"/"+file_name, ContentFile(''))
        output_file_row = default_storage.save(settings.MEDIA_ROOT+"/"+path+"/"+file_name_unchanged, ContentFile(''))
        
        #cnr_doc_df = cnr_doc_df.astype('float32')
        cnr_doc_df.to_excel(output_file,sheet_name='CNR')
        #cnr_unchanged_df = cnr_unchanged_df.astype('float32')
        #cnr_unchanged_df.to_excel(output_file_row,sheet_name='CNR')
        
        """
        with ExcelWriter(output_file, engine='xlsxwriter') as writer:
            cnr_doc_df.to_excel(writer,'CNR')
       
        with ExcelWriter(output_file_row, engine='xlsxwriter') as writer:
            cnr_unchanged_df.to_excel(writer,'CNR')   
        """
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


from mpl_toolkits.axes_grid1 import AxesGrid
import csv
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import matplotlib as mpl


def shiftedColorMap(cmap, start=0, midpoint=0, stop=1.0, name='shiftedcmap'):
    '''
    Function to offset the "center" of a colormap. Useful for
    data with a negative min and positive max and you want the
    middle of the colormap's dynamic range to be at zero

    Input
    -----
      cmap : The matplotlib colormap to be altered
      start : Offset from lowest point in the colormap's range.
          Defaults to 0.0 (no lower ofset). Should be between
          0.0 and `midpoint`.
      midpoint : The new center of the colormap. Defaults to 
          0.5 (no shift). Should be between 0.0 and 1.0. In
          general, this should be  1 - vmax/(vmax + abs(vmin))
          For example if your data range from -15.0 to +5.0 and
          you want the center of the colormap at 0.0, `midpoint`
          should be set to  1 - 5/(5 + 15)) or 0.75
      stop : Offset from highets point in the colormap's range.
          Defaults to 1.0 (no upper ofset). Should be between
          `midpoint` and 1.0.
    '''
    cdict = {
        'red': [],
        'green': [],
        'blue': [],
        'alpha': []
    }

    # regular index to compute the colors
    reg_index = np.linspace(start, stop, 257)

    # shifted index to match the data
    shift_index = np.hstack([
        np.linspace(0.0, midpoint, 128, endpoint=False), 
        np.linspace(midpoint, 1.0, 129, endpoint=True)
    ])

    for ri, si in zip(reg_index, shift_index):
        r, g, b, a = cmap(ri)

        cdict['red'].append((si, r, r))
        cdict['green'].append((si, g, g))
        cdict['blue'].append((si, b, b))
        cdict['alpha'].append((si, a, a))

    newcmap = mpl.colors.LinearSegmentedColormap(name, cdict)
    plt.register_cmap(cmap=newcmap)

    return newcmap

    
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
        
        
        ppp = Pathway.objects.get(name='HA_syntesis_pathway', organism='human', database='primary_new', amcf=0)
        
        
        
        
        df_rel = read_csv(settings.MEDIA_ROOT+'/HA_syntesis_pathway_interactions.csv')
        
        def add_rels(col):
            
            fr_node = Node.objects.get(name=col['From node'], pathway=ppp)
            to_node = Node.objects.get(name=col['To node'], pathway=ppp)
            
            if col['Relation type']=='activation':
                reltype=1
            elif col['Relation type']=='inhibition':
                reltype=0
            else:
                reltype=2
            mr = Relation(fromnode=fr_node, tonode=to_node, reltype=reltype)
                
            mr.save()
            
       
        
        dd = df_rel.apply(add_rels, axis=1)
        raise Exception('test stop')
        
        df1=read_csv(settings.MEDIA_ROOT+'/nodes-comp-biocarta.csv')
        df1 = df1.T.drop_duplicates().T
        def mazafaka(row):
            
            nnn = row.name
            print " ----  "+nnn
            row = row.dropna()
            row = row.tolist()
            row.sort()
            
            
            for col in df1:
                ss = df1[col]
                
                ss = ss.dropna()
                ss = Series(ss)
                ss = ss.tolist()
                ss.sort()
                
                
                
                
                if row==ss:
                    
                    nnodes = Node.objects.filter(name=col, pathway__database='biocarta')
                    for nnode in nnodes:
                        nnode.name = nnn
                        nnode.save()  
                    #raise Exception('inner stop')
        
             
        for subdir, dirs, files in os.walk(settings.MEDIA_ROOT+'/renamed pathways proteins/'):
            ff = files
        i=0
        ff.sort()
        for ffile in ff:
            i=i+1
            print ffile+'   n='+str(i)
            try:
                df = read_csv(settings.MEDIA_ROOT+'/renamed pathways proteins/'+ffile)
                
                
                df.apply(mazafaka)
            except:
                #raise
                print "ERROR in "+ffile
                
                
        raise Exception('stop')
        
        """ HUMAN PATH TO MOUSE
        for mmm in Pathway.objects.filter(organism='mouse', database='kegg_adjusted'):
            mmm.delete()
        
        hps = Pathway.objects.filter(organism='human', database='kegg_adjusted')
        i=0
        for hp in hps:
            i=i+1
            print hp.name+' i = '+str(i)
            
            mp = Pathway(organism='mouse', database='kegg_adjusted', name=hp.name, amcf=hp.amcf)
            mp.save()
            
            for hg in hp.gene_set.all():
                try:
                    mmap = MouseMapping.objects.filter(human_gene_symbol=hg.name)[0]
                
                    mg = Gene(name=mmap.mouse_gene_symbol.upper(), arr=hg.arr, pathway=mp, comment=hg.comment)
                except:
                    mg = Gene(name=hg.name, arr=hg.arr, pathway=mp, comment=hg.comment)
                    
                mg.save()
                
            for hn in hp.node_set.all():
                mn = Node(name=hn.name, comment=hn.comment, pathway=mp)
                mn.save()
                for hc in hn.component_set.all():
                    try:
                        mmap = MouseMapping.objects.filter(human_gene_symbol=hc.name)[0]
                        mc = Component(name=mmap.mouse_gene_symbol.upper(), node=mn)
                        
                    except:
                        mc = Component(name=hc.name, node=mn)
                    mc.save()
                    
            
            for hn in hp.node_set.all():
                for inrel in hn.inrelations.all():
                    mfn = Node.objects.filter(name=inrel.fromnode.name, pathway=mp)[0]
                    mtn = Node.objects.filter(name=inrel.tonode.name, pathway=mp)[0]
                    mr = Relation(fromnode=mfn, tonode=mtn)
                    mr.save()
        """
        
        
        """
        df = read_excel(settings.MEDIA_ROOT+"/report/output_PAS_crispr_resultcpoolmerged_both_rev_metabolism_primary.xlsx", sheetname='PAS1' )
        
        df_s = df[df['Database']=='primary_new']
        df_s = df_s[['New Pathway name', 'Low GFP-p62', 'High GFP-p62']]
        df_s.columns=['name', 'x', 'y']
        
        df_m = df[df['Database']=='metabolism']
        df_m = df_m[['New Pathway name', 'Low GFP-p62', 'High GFP-p62']]
        df_m.columns=['name', 'x', 'y']
        
        df_s_up = df_m.sort(['x'], ascending=False)
        df_s_up = df_s_up.head(n=10)
        
        uup = df_s_up.to_json(settings.MEDIA_ROOT+"/report/path/metabolism_low_up.json", orient='values')
        
        df_s_down = df_m.sort(['x'], ascending=True)
        df_s_down = df_s_down.head(n=10)
        
        ddown = df_s_down.to_json(settings.MEDIA_ROOT+"/report/path/metabolism_low_down.json", orient='values')
        
        raise Exception('stop12')
        
        p_s = df_s.to_json( orient='records')
        p_s1 = json.loads(p_s)
        lp_s = []
        p_s1 = yaml.safe_load(p_s)
        for xxx in p_s1:
            xxx['x'] = float(xxx['x'])
            xxx['y'] = float(xxx['y'])
            xxx= json.dumps(xxx)
            lp_s.append(xxx)
        
        f = open(settings.MEDIA_ROOT+"/path1.json", "w")
        f.write(",".join(map(lambda x: str(x), lp_s)))
        f.close()
        
        
        
        p_m = df_m.to_json( orient='records')
        p_m1 = json.loads(p_m)
        lp_m = []
        p_m1 = yaml.safe_load(p_m)
        for xxx in p_m1:
            xxx['x'] = float(xxx['x'])
            xxx['y'] = float(xxx['y'])
            xxx= json.dumps(xxx)
            lp_m.append(xxx)
            
        f = open(settings.MEDIA_ROOT+"/path2.json", "w")
        f.write(",".join(map(lambda x: str(x), lp_m)))
        f.close()
        """
        # GENE TABLES 
        
        dfp = read_csv(settings.MEDIA_ROOT+"/report/res_low_vs_high_genes.csv")
        pval = dfp[dfp['pval']<0.05]
        pval.rename(columns={'Gene': 'SYMBOL'}, inplace=True)
        pval.set_index('SYMBOL', inplace=True)
        
        df = read_csv(settings.MEDIA_ROOT+"/report/crispr_resultcpoolmerged_log2.txt", sep='\t')
        
        df_1 = df
        df_1.set_index('SYMBOL', inplace=True)
        
        joined = df_1.join(pval, how='inner')
        joined.reset_index(inplace=True)
        
        df_1 = joined[['SYMBOL', 'Low GFP-p62', 'High GFP-p62' ]]
        
        
        df_1.columns = ['name', 'x', 'y' ]
        jjj = df_1.to_json( orient='records')
        
        #jjj = jjj.replace('"x"', 'x').replace('"y"', 'y').replace('"name"', 'name')
        jjj1 = json.loads(jjj)
        
        lll = []
        jjj1 = yaml.safe_load(jjj)
        for xxx in jjj1:
            xxx['x'] = float(xxx['x'])
            xxx['y'] = float(xxx['y'])
            xxx= json.dumps(xxx)
            lll.append(xxx)
            
            
            
        
        
        f = open(settings.MEDIA_ROOT+"/genes-low-high.json", "w")
        f.write(",".join(map(lambda x: str(x), lll)))
        f.close()
        #"""
        raise Exception('stop')
        """ MOUSE TOPOLOGY
        for hp in Pathway.objects.filter(organism='human', database='primary_old').exclude(name__in=['AHR_Pathway', 'AHR_Pathway_AHR_Degradation', 'AHR_Pathway_Cath_D_Expression', 'AHR_Pathway_C_Myc_Expression', 'AHR_Pathway_PS2_Gene_Expression']):
            mp = Pathway.objects.get(organism='mouse', database='primary_old', name=hp.name)
            
            print mp.name
            
            for hn in hp.node_set.all():
                mn = Node(name=hn.name, comment=hn.comment, pathway=mp)
                mn.save()
                for hc in hn.component_set.all():
                    try:
                        mmap = MouseMapping.objects.filter(human_gene_symbol=hc.name)[0]
                        mc = Component(name=mmap.mouse_gene_symbol.upper(), node=mn)
                        mc.save()
                    except:
                        pass
                    
            
            for hn in hp.node_set.all():
                for inrel in hn.inrelations.all():
                    mfn = Node.objects.get(name=inrel.fromnode.name, pathway=mp)
                    mtn = Node.objects.get(name=inrel.tonode.name, pathway=mp)
                    mr = Relation(fromnode=mfn, tonode=mtn)
                    mr.save()
        """
        #raise Exception('stop')
        """XML PATHS """
        from lxml import etree
        
        res_file = settings.MEDIA_ROOT+"/symbol_number.txt"
        with open(res_file, 'rb') as csvfile:
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(csvfile.read(), delimiters='\t,;')
            csvfile.seek(0)
        mapping = read_csv(res_file, delimiter=dialect.delimiter, names=['number', 'gene'] )
         
        mapping.set_index('gene',inplace=True)
        
        i=0
        for path in Pathway.objects.filter(organism='mouse', database='primary_old'):
            root = etree.Element("pathway", name=path.name, title=path.name, org="hsa", number=str(path.id))  
            i=i+1
            print path.name+" i="+str(i)
            zero_nodes = []
            for node in path.node_set.all():
                
                graph = []
                entrezGene = []
                
                
                for comp in node.component_set.all():
                    try:
                        graph.append(comp.name.strip())
                        entrezGene.append("hsa:"+str(mapping.loc[comp.name.strip()]['number']))
                    except:
                        pass
                if len(entrezGene)>0:
                    entry = etree.SubElement(root, "entry", id=str(node.id), name=', '.join(entrezGene), type="gene")
                    graph_comp = etree.SubElement(entry, "graphics", name=', '.join(graph), 
                                              fgcolor="#000000", bgcolor="#BFFFBF", type="rectangle",
                                              x="10", y="10", width="10", height="10" )
                    
                else:
                    zero_nodes.append(node.id)
                    
            #raise Exception('fire')
            for node in path.node_set.all():    
                for inrel in node.inrelations.all():
                        if inrel.reltype == '1':
                            relColor = 'activation'
                        if inrel.reltype == '0':
                            relColor = 'inhibition'
                        if (inrel.fromnode.id not in zero_nodes) and (inrel.tonode.id not in zero_nodes): 
                            relation = etree.SubElement(root, "relation", entry1=str(inrel.fromnode.id),
                                                 entry2=str(inrel.tonode.id), type='PPrel')
                            subtype = etree.SubElement(relation, "subtype", name=relColor, value="--|")
                
                
            applic = open(settings.MEDIA_ROOT+"/xmlpaths/mouse/primary_old/"+path.name+".xml", "w")
            for parent in root.xpath('//*[./*]'): # Search for parent elements
                parent[:] = sorted(parent,key=lambda x: x.tag)
            handle = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True)
            applic.writelines(handle)
            applic.close()
        raise Exception('XML')
        """ """
        
        """ breast module statistics
        import collections
        for fn in os.listdir(settings.MEDIA_ROOT+"/diffparams/"):
            xpn_df = read_csv(settings.MEDIA_ROOT+"/diffparams/"+fn, index_col=0).fillna('NONE')
            lpath = []
            for col in xpn_df.columns:
                lpath+=xpn_df[col].values.tolist()
            counter=collections.Counter(lpath)
            most = counter.most_common(len(xpn_df.index)+1)
            stat = []
            for val in most:
                if val[0]!='NONE':
                    dstat = {'pathway': val[0],
                             'repeat frequency': val[1]}
                    stat.append(dstat)
            result = DataFrame(stat)
            result.to_csv(settings.MEDIA_ROOT+"/statProcessed/diffparams/"+fn)          
        """
        """ add new pathways for aliper 
        for fn in os.listdir(settings.MEDIA_ROOT+"/newpaths/"):
            pathname = "z_"+fn.split(".")[0]
            p = Pathway(name=pathname, amcf=0)
            p.save()
            gene_df = read_excel(settings.MEDIA_ROOT+"/newpaths/"+fn )
            
            for index, row in gene_df.iterrows():
                g = Gene(name = row['gene'], arr=row['arr'], pathway=p)
                g.save()
        """
            
        

        
        new_path_df = read_excel(settings.MEDIA_ROOT+"/primary_new_pathways_renaming.xlsx",
                                         sheetname=0, header=None)
        new_path_df.columns=['Old Pathway Name', 'Pathway Name']
        new_path_df.set_index('Old Pathway Name', inplace=True)
        dict = {}
        lname = []
        lgene = []
        pathways = Pathway.objects.filter(organism='human', database='metabolism')
        for path in pathways:
            
            
            try:                    
                new_path_name = new_path_df.loc[path.name.strip()]['Pathway Name']
                   
            except KeyError:
                new_path_name = path.name
            
            for gene in path.gene_set.all():
                lname.append(new_path_name)
                lgene.append(gene.name)
                #dict[new_path_name] = gene.name
            
        dict['Pathway'] =  lname
        dict['Gene'] = lgene   
        df = DataFrame(dict)
        df.to_csv('pathways_genes_metabolism.csv')
        raise Exception('stop')
    
    
    
    
        import networkx as nx
        import struct
       
        
        
        
        
        def colormap(col, path):
            if col.name=='x':
                col = col.fillna(0)
                mmin = np.min(col)
                mmax = np.max(col)
                
                if mmax<0 and mmin<0:
                    
                    shifted_cmap = plt.get_cmap('Blues_r')
                else:
                    mid = 1 - mmax/(mmax + abs(mmin))
                    
                    cmap = plt.get_cmap('coolwarm')
                    shifted_cmap = shiftedColorMap(cmap, start=0.15, midpoint=mid, stop=0.85, name='shrunk')
                fig = plt.figure(figsize=(8,3))
                ax1 = fig.add_axes([0.05, 0.80, 0.9, 0.15])                          
                
                
                cNormp  = colors.Normalize(vmin=mmin, vmax=mmax)
                scalarMap = cmx.ScalarMappable(norm=cNormp, cmap=shifted_cmap)
                
                cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=shifted_cmap,
                                   norm=cNormp,
                                   orientation='horizontal')
                cb1.set_label('nodes activation')
        
                #plt.savefig('nicolay/'+path.name+'/'+path.name+'_scale.png')
                plt.savefig('denis/'+path.name+'/'+path.name+'_scale.png')    
                 
                G=nx.DiGraph()
                 
                for node, value in col.iteritems():
                    if value!=0:
                        ffil = "#"+struct.pack('BBB',*scalarMap.to_rgba(value, bytes=True)[:3]).encode('hex').upper()
                    else:
                        ffil="#ffffff"
                    G.add_node(node, color='black',style='filled',
                               fillcolor=ffil)
                
                for node in path.node_set.all():
                    for inrel in node.inrelations.all():
                        if inrel.reltype == '1':
                            relColor = 'green'
                        if inrel.reltype == '0':
                            relColor = 'red'
                        G.add_edge(inrel.fromnode.name.encode('ascii','ignore'), inrel.tonode.name.encode('ascii','ignore'), color=relColor)
                 
                nx.draw_graphviz(G)
                nx.write_dot(G, 'denis/'+path.name+'/'+path.name+'.dot')
                A=nx.to_agraph(G)
                A.layout(prog='dot')
                A.draw('denis/'+path.name+'/'+path.name+'_'+col.name+'.svg')
            
                #raise Exception('color')
        lpaths = ['Wnt_Pathway',
                  'VEGF_Pathway',
                  'Ubiquitin_Proteasome_Pathway',
                  'TRAF_m_Pathway',
                  'TNF_m_Pathway',
                  'TGF_beta_Pathway',
                  'STAT3_Pathway',
                  'SMAD_m_Pathway',
                  'RAS_Pathway',
                  'RANK_Signaling_in_Osteoclast_Pathway',
                  'PTEN_Pathway',
                  'PAK_Pathway',
                  'p38_m_Signaling_Pathway',
                  'Notch_Pathway',
                  'NGF_p_Pathway',
                  'NGF_m_Pathway',
                  'mTOR_Pathway',
                  'Mitochondrial_Apopotosis_m_Pathway',
                  'Mismatch_Repair_Pathway',
                  'MAPK_Signaling_Pathway',
                  'MAPK_Family_Pathway',
                  'JNK_Pathway',
                  'JAK_mStat_Pathway',
                  'IP3_Pathway',
                  'Interferon_Pathway',
                  'ILK_Pathway',
                  'IL_10_Pathway',
                  'IL_6_Pathway',
                  'IL_2_Pathway',
                  'IGF1R_Signaling_Pathway',
                  'HGF_Pathway',
                  'Hedgehog_Pathway',
                  'GSK3_Pathway',
                  'Growth_Hormone_Pathway',
                  'GPCR_Pathway',
                  'Glucocorticoid_Receptor_Pathway',
                  'FLT3_Signaling_Pathway',
                  'Estrogen_Pathway',
                  'Erythropoeitin_Pathway',
                  'ERK_Signaling_Pathway',
                  'ErbB_Family_Pathway',
                  'EGFR1_Pathway',
                  'Cytokine_Network_Pathway',
                  'Circadian_Pathway',
                  'Chemokine_Pathway',
                  'cAMP_Pathway',
                  'ATM_Pathway',
                  'AKT_Pathway',
                  'AHR_Pathway'
                  ]
        lpaths1 = ['p38_p_Signaling_Pathway', 'SMAD_p_Pathway'  ]
        lfrag = ['AHR_Pathway',
                 'AKT_Pathway',
                 'ATM_Pathway',
                 'cAMP_Pathway',
                 'Caspase_Cascade',
                 'CD40_Pathway',
                 'Cellular_Anti_Apoptosis_Pathway',
                 'Chemokine_Pathway',
                 'Chromatin_Pathway',
                 'Circadian_Pathway',
                 'CREB_Pathway',
                 'Cytokine_Network_Pathway',
                 'EGFR1_Pathway',
                 'ErbB_Family_Pathway',
                 'ERK_Signaling_Pathway',
                 'Erythropoeitin_Pathway',
                 'Estrogen_Pathway',
                 'FLT3_Signaling_Pathway',
                 'Glucocorticoid_Receptor_Pathway',
                 'GPCR_Pathway',
                 'Growth_Hormone_Pathway',
                 'GSK3_Pathway',
                 'Hedgehog_Pathway',
                 'HGF_Pathway',
                 'HIF1Alpha_Pathway',
                 'IGF1R_Signaling_Pathway',
                 'IL_2_Pathway',
                 'IL_6_Pathway',
                 'IL_10_Pathway',
                 'ILK_Pathway',
                 'Interferon_Pathway',
                 'IP3_Pathway',
                 'JAK_mStat_Pathway',
                 'JNK_Pathway',
                 'MAPK_Family_Pathway',
                 'MAPK_Signaling_Pathway',
                 'Mismatch_Repair_Pathway',
                 'Mitochondrial_Apopotosis_m_Pathway',
                 'mTOR_Pathway',
                 'NGF_m_Pathway',
                 'NGF_p_Pathway',
                 'Notch_Pathway',
                 'p38_m_Signaling_Pathway',
                 'p38_p_Signaling_Pathway',
                 'p53_Signaling_m_Pathway',
                 'PAK_Pathway',
                 'PPAR_Pathway',
                 'PTEN_Pathway',
                 'RANK_Signaling_in_Osteoclast_Pathway',
                 'RAS_Pathway',
                 'SMAD_m_Pathway',
                 'SMAD_p_Pathway',
                 'STAT3_Pathway',
                 'TGF_beta_Pathway',
                 'TNF_m_Pathway',
                 'TNF_p_Pathway',
                 'TRAF_m_Pathway',
                 'TRAF_p_Pathway',
                 'Ubiquitin_Proteasome_Pathway',
                 'VEGF_Pathway',
                 'Wnt_Pathway']
        lpath2 = ['p53_Signaling_m_Pathway']
        for p in lpath2:
            path = Pathway.objects.get(name=p, database='primary_old', organism='human')
           

            filename = settings.MEDIA_ROOT+"/denis/"+p+"_signed_AUC_mod.txt.csv"
        
            df_my_nodes = read_excel(settings.MEDIA_ROOT+"/nodes/"+p+".xlsx", sheetname="nodes" )
            nodes = list(df_my_nodes.columns.values)
            
            
            
            df_nicolay_nodes = read_csv(filename, index_col=0 )
            df_nicolay_nodes.index.name = 'SYMBOL'
            df_nicolay_nodes['nodes'] = nodes
            df_nicolay_nodes = df_nicolay_nodes.set_index('nodes')
            df_nicolay_nodes.columns = ['x']
            #raise Exception('test')
            
            os.mkdir('denis/'+path.name)
            df_nicolay_nodes.apply(colormap,path=path, axis=0)


        
        raise Exception('yoyyo1')
        
        
        
        
        raise Exception('test')
        return context



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
