# -*- coding: utf-8 -*-
import os
import math
import csv
from datetime import datetime
from pandas import read_csv, read_excel, DataFrame, Series, ExcelWriter
import numpy as np

from django.views.generic.edit import FormView #CreateView , UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.files import File
from django.core.exceptions import MultipleObjectsReturned
from django.conf import settings

from .forms import  CalculationParametersForm
from profiles.models import Document, ProcessDocument
from database.models import Pathway, Gene, Drug
from metabolism.models import MetabolismPathway, MetabolismGene
from mouse.models import MousePathway, MouseGene


class CoreSetCalculationParameters(FormView):
    """
    Processes the form with calculation parameters, creates empty output Document, 
    creates Document in Process directory with PANDAS column 'Mean_Norm' and CNR for each gene     
    """
    form_class = CalculationParametersForm
    template_name = 'core/core_calculation_parameters.html'
    success_url = '/success/'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):        
        return super(CoreSetCalculationParameters, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(CoreSetCalculationParameters, self).get_context_data(**kwargs)
        
        input_document = Document.objects.get(pk=self.kwargs['pk'])
        
        context['document'] = input_document
        return context
    
    def form_valid(self, form):
        sigma_num = form.cleaned_data['sigma_num']
        use_sigma = form.cleaned_data['use_sigma']
        cnr_low =  form.cleaned_data['cnr_low']
        cnr_up =  form.cleaned_data['cnr_up']
        use_cnr = form.cleaned_data['use_cnr']
        norm_choice = form.cleaned_data['norm_choice']
        db_choice = form.cleaned_data['db_choice']
        calculate_pms = form.cleaned_data['calculate_pms']
        calculate_pms1 = form.cleaned_data['calculate_pms1']
        calculate_ds1 = form.cleaned_data['calculate_ds1']
        calculate_ds2 = form.cleaned_data['calculate_ds2']
        calculate_norms_pas = form.cleaned_data['calculate_norms_pas']
        calculate_pvalue_each = form.cleaned_data['calculate_pvalue_each']
        calculate_pvalue_all = form.cleaned_data['calculate_pvalue_all'] 
        
        
        context = self.get_context_data()
        
        """ update current Input Document """
        input_document = context['document']
        input_document.calculated_by = self.request.user
        input_document.calculated_at = datetime.now()
        input_document.save()
        
        """ Create an empty Output Document  """
        
        if not os.path.exists(settings.MEDIA_ROOT+'/'+os.path.join('users', str(input_document.project.owner),
                                            str(input_document.project),'output')):
            os.mkdir(settings.MEDIA_ROOT+'/'+os.path.join('users', str(input_document.project.owner),
                                            str(input_document.project),'output'))
        
        output_doc = Document()        
        output_doc.doc_type = 2
        if int(db_choice) == 1:
            json_db = 'Human'
        elif int(db_choice) == 2:
            json_db = 'Mouse'
        elif int(db_choice) == 3:
            json_db = 'Metabolism'
        output_doc.parameters = {'sigma_num': sigma_num,
                                 'use_sigma': use_sigma,
                                 'cnr_low': cnr_low,
                                 'cnr_up': cnr_up,
                                 'use_cnr': use_cnr,
                                 'norm_algirothm': 'geometric' if int(norm_choice)>1 else 'arithmetic',
                                 'db': json_db }
        output_doc.project = input_document.project
        output_doc.created_by = self.request.user
        output_doc.created_at = datetime.now()        
        #output_doc.save()
        
                
        
        """ Calculating PMS and PMS1 """
         
        def strip(text):
            try:
                return text.strip().upper()
            except AttributeError:
                return text
        
        calculate_p_value = False # Flag for p-value calculation 
         
        if input_document.norm_num >= 4:
            calculate_p_value = True        
            filename = settings.MEDIA_ROOT+"/"+input_document.document.name
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(open(filename, 'r').read(), delimiters='\t,;') # defining the separator of the csv file
            input_doc_df = read_csv(filename, delimiter=dialect.delimiter, index_col='SYMBOL',
                                                                   converters = {'SYMBOL' : strip})
                
            input_doc_df = input_doc_df.groupby(input_doc_df.index, level=0).mean()
        
           
            norms_df = input_doc_df[[col for col in input_doc_df.columns if 'Norm' in col]]
            
            
            def calculate_norms_cnr(x, df):
                only_norms_df = df.drop(x.name, axis=1) # exclude current column from new DatFrame
                mean_df = only_norms_df.mean(axis=1)
                output = x.div(mean_df, axis='index')
                return output
                
            
            norms_df = norms_df.apply(calculate_norms_cnr, axis=0, df=norms_df)   
                
                
        
        process_doc_df = read_csv(settings.MEDIA_ROOT+"/"+input_document.input_doc.document.name,
                                  sep='\t', index_col='SYMBOL',  converters = {'SYMBOL' : strip})        
        
        tumour_columns = [col for col in process_doc_df.columns if 'Tumour' in col] #get sample columns
        
        pms_list = []
        pms1_list = []
        differential_genes = {}
        
        if int(db_choice) == 1:
            pathway_objects = Pathway.objects.all() # Human DB
        elif int(db_choice) == 2:
            pathway_objects = MetabolismPathway.objects.all() # Metabolism DB
        elif int(db_choice) == 3:
            pathway_objects = MousePathway.objects.all() # Mouse DB
                
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
            
            joined_df = gene_df.join(process_doc_df, how='inner')
            
            
            pms_dict = {}
            pms1_dict = {}
            
            pms_dict['Pathway'] = pms1_dict['Pathway'] = pathway.name.strip()
            
            """ Calculating PAS for Normal Values. All genes are assumed to be differential """
            if calculate_p_value and (calculate_pvalue_each or calculate_pvalue_all):
                
               
                
                joined_df_norms = gene_df.join(norms_df, how='inner')
                
                
                def calculate_norms_pms(col, arr, cnr_low, cnr_up):
                    if 'Norm' in col.name:
                        
                        
                        col = col[(col>cnr_up) | (col<cnr_low)] # CNR FILTER
                        return np.log(col)*arr
                       
                    else:
                        return col # in case it's ARR column
                
                
                
                pms_norms = joined_df_norms.apply(calculate_norms_pms, axis=0, 
                                                  arr=joined_df_norms['ARR'], 
                                                  cnr_low=cnr_low, cnr_up=cnr_up).fillna(0)
                
                
                lnorms_p_value = []
                for norm in [x for x in pms_norms.columns if 'Norm' in x]:
                    pms1_value = pms_norms[norm].sum()
                    if calculate_norms_pas:
                        pms_dict[norm] = float(pathway.amcf)*pms_norms[norm].sum()
                        pms1_dict[norm] = pms1_value
                    lnorms_p_value.append(pms1_value)
                
                    
                          
            
            
            
            
            raise
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
                        mean = row['Mean_norm']
                        EXPRESSION_LEVEL = CNR*float(mean)
                         
                    if int(norm_choice) == 2:
                        mean = row['gMean_norm']
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
                
                pms1_all.append(summ)
                
                if calculate_p_value and calculate_pvalue_each:
                    from scipy.stats import ttest_1samp  
                    z_stat, p_val = ttest_1samp(lnorms_p_value, summ)
                    pms1_dict[tumour+'_p-value'] = p_val               
            
            if calculate_p_value and calculate_pvalue_all:
                    from scipy.stats import ranksums  
                    z_stat, p_val = ranksums(lnorms_p_value, pms1_all)
                    pms1_dict['p-value_Mean'] = p_val 
                
            pms_list.append(pms_dict)
            pms1_list.append(pms1_dict)        
        
        output_pms_df = DataFrame(pms_list)
        output_pms_df = output_pms_df.set_index('Pathway')
        output_pms1_df = DataFrame(pms1_list)
        output_pms1_df = output_pms1_df.set_index('Pathway')
        
        """ Calculating Drug Score """
        output_ds1_df = output_ds2_df = DataFrame()
        
        if (calculate_ds1 or calculate_ds2):
            ds1_list = []
            ds2_list = []
        
            for drug in Drug.objects.all(): #iterate trough all Drugs
                ds1_dict = {}
                ds2_dict = {}
                ds1_dict['Drug'] = ds2_dict['Drug'] = drug.name.strip()
                ds1_dict['DataBase'] = ds2_dict['DataBase'] = drug.db
                ds1_dict['Type'] = ds2_dict['Type'] = drug.tip
            
            
            
                for tumour in tumour_columns: #loop thought samples columns
                    DS1 = 0 # DrugScore 1
                    DS2 = 0 # DrugScore 2
            
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
                                PMS = output_pms_df.at[path.name, tumour]
                                AMCF = float(path.amcf)
                            
                                if drug.tip == 'inhibitor' and path.name!='Mab_targets':
                                    DS1 += PMS
                                    DS2 += AMCF*ARR*math.log10(CNR)
                                if drug.tip == 'activator' and path.name!='Mab_targets':
                                    DS1 -= PMS
                                    DS2 -= AMCF*ARR*math.log10(CNR)
                                if drug.tip == 'mab' and path.name!='Mab_targets':
                                    DS1 += PMS
                                    DS2 += AMCF*ARR*math.log10(CNR)
                                if drug.tip == 'mab' and path.name=='Mab_targets':
                                    DS1 += abs(PMS) # PMS2
                                if drug.tip == 'killermab' and path.name=='Mab_targets':
                                    DS1 += abs(PMS)# PMS2
                                    DS2 += math.log10(CNR)
                                if drug.tip == 'multivalent' and path.name!='Mab_targets':
                                    DS1 += PMS
                                    if target.tip>0:
                                        DS2 -= AMCF*ARR*math.log10(CNR)
                                    else:
                                        DS2 += AMCF*ARR*math.log10(CNR)
                                    
                    ds1_dict[tumour] = DS1
                    ds2_dict[tumour] = DS2
            
                ds1_list.append(ds1_dict)
                ds2_list.append(ds2_dict)
            
            output_ds1_df = DataFrame(ds1_list)
            output_ds1_df = output_ds1_df.set_index('Drug')
            output_ds2_df = DataFrame(ds2_list)
            output_ds2_df = output_ds2_df.set_index('Drug')
        
               
                    
        """ Saving results to Excel file and to database """
        path = os.path.join('users', str(input_document.project.owner),
                                            str(input_document.project),'output')
        file_name = 'output_'+str(input_document.get_filename()+'.xlsx')
        
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        
        output_file = default_storage.save(settings.MEDIA_ROOT+"/"+path+"/"+file_name, ContentFile(''))
                
        with ExcelWriter(output_file, index=False) as writer:
            if calculate_pms:
                output_pms_df.to_excel(writer,'PMS')
            if calculate_pms1:     
                output_pms1_df.to_excel(writer,'PMS1')
            if calculate_ds1:
                output_ds1_df.to_excel(writer, 'DS1')
            if calculate_ds2:
                output_ds2_df.to_excel(writer, 'DS2')
        
        
        output_doc.document = path+"/"+os.path.basename(output_file)
        output_doc.related_doc = input_document
        output_doc.save() 
         
        
        
        
        
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
        
        #from .tasks import add
        
        #res = add.delay(1,1)
        
        path = os.path.join('users', "Misha",
                                            "newnewnew", 'output_test.xlsx')
        
        
        d = {'one' : Series([1., 2., 3.], index=['a', 'b', 'c']),
             'two' : Series([1., 2., 3., 4.], index=['a', 'b', 'c', 'd'])}
        
        df = DataFrame(d)
        
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile      
      
        
        path1 = default_storage.save(settings.MEDIA_ROOT+"/"+path, ContentFile(''))
        
        writer = ExcelWriter(path1, index=False)
        
        df.to_excel(path1,'PMS')
        
        
        
        
        
        """
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
        
        context['task_id'] = path1
        
        
        
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
