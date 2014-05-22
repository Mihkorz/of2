# -*- coding: utf-8 -*-
import os
import math
import csv
from datetime import datetime
from pandas import read_csv, DataFrame, ExcelWriter

from django.views.generic.edit import FormView #CreateView , UpdateView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.files import File
from django.conf import settings

from .forms import  CalculationParametersForm
from profiles.models import Document, ProcessDocument
from database.models import Pathway, Gene, Drug


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
        output_doc.parameters = {'sigma_num': sigma_num,
                                 'use_sigma': use_sigma,
                                 'cnr_low': cnr_low,
                                 'cnr_up': cnr_up,
                                 'use_cnr': use_cnr }
        output_doc.project = input_document.project
        output_doc.created_by = self.request.user
        output_doc.created_at = datetime.now()        
        #output_doc.save()
                
        
        """ Calculating PMS and PMS1 """
         
        def strip(text):
            try:
                return text.strip()
            except AttributeError:
                return text
        
        process_doc_df = read_csv(settings.MEDIA_ROOT+"/"+input_document.input_doc.document.name,
                                  sep='\t', index_col='SYMBOL',  converters = {'SYMBOL' : strip})        
        
        tumour_columns = [col for col in process_doc_df.columns if 'Tumour' in col] #get sample columns
        
        pms_list = []
        pms1_list = []
        differential_genes = []
        
        for pathway in Pathway.objects.all():
            gene_name = []
            gene_arr = []
            for gene in pathway.gene_set.all():
                gene_name.append(gene.name.strip())
                gene_arr.append(gene.arr)
            
            gene_data = {'SYMBOL': gene_name,
                         'ARR': gene_arr}
            
            gene_df = DataFrame(gene_data)
            gene_df = gene_df.set_index('SYMBOL') #create index by SYMBOL column
            
            joined_df = gene_df.join(process_doc_df, how='inner')
            
            pms_dict = {}
            pms1_dict = {}
            
            pms_dict['Pathway'] = pms1_dict['Pathway'] = pathway.name.strip()
            
            
            for tumour in tumour_columns: #loop thought samples columns                
                summ = 0
                for index, row in joined_df.iterrows():
                    if not use_sigma:
                        sigma_num = 0
                    if not use_cnr:
                        cnr_up = cnr_low = 0
                        
                    if (row[tumour]*row['Mean_norm'] > (row['Mean_norm']+sigma_num*row['std']) or  \
                        row[tumour]*row['Mean_norm'] < (row['Mean_norm']-sigma_num*row['std'])) and \
                       (row[tumour]>cnr_up or row[tumour]<cnr_low) and \
                       row[tumour]>0:
                        
                        summ+= float(row['ARR'])*math.log(row[tumour]) # ARR*ln(CNR)
                        
                        differential_genes.append(index) # store differential genes in a list
                
                pms_dict[tumour] = float(pathway.amcf)*summ #PMS
                pms1_dict[tumour] = summ #PMS1               
                
            pms_list.append(pms_dict)
            pms1_list.append(pms1_dict)        
        
        output_pms_df = DataFrame(pms_list)
        output_pms_df = output_pms_df.set_index('Pathway')
        output_pms1_df = DataFrame(pms1_list)
        output_pms1_df = output_pms1_df.set_index('Pathway')
        
        """ Calculating Drug Score """
        
        ds1_list = []
        ds2_list = []
        
        for drug in Drug.objects.all(): #iterate trough all Drugs
            ds1_dict = {}
            ds2_dict = {}
            ds1_dict['Drug'] = ds2_dict['Drug'] = drug.name.strip()
            
            DS1 = 0 # DrugScore 1
            DS2 = 0 # DrugScore 2
            
            for tumour in tumour_columns: #loop thought samples columns
            
                for target in drug.target_set.all():
                    target.name = target.name.strip()
                    if target.name in differential_genes:
                        pathways = Pathway.objects.filter(gene__name=target.name)
                    
                        for path in pathways:
                            gene = Gene.objects.get(name = target.name ,pathway=path)
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
                                            str(input_document.project),'output', 'output_'+str(input_document.get_filename()+'.xlsx'))
        output_file = File(settings.MEDIA_ROOT+"/"+path)
        
        writer = ExcelWriter(output_file.file, index=False)
        output_pms_df.to_excel(writer,'PMS')
        output_pms1_df.to_excel(writer,'PMS1')
        output_ds1_df.to_excel(writer, 'DS1')
        output_ds2_df.to_excel(writer, 'DS2')
        writer.save()
        
        output_doc.document = path
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
        
