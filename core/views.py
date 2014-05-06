# -*- coding: utf-8 -*-
import os
import math
from datetime import datetime
from pandas import read_csv, DataFrame

from django.views.generic.edit import FormView #CreateView , UpdateView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

from .forms import  CalculationParametersForm
from profiles.models import Document, ProcessDocument
from database.models import Pathway, Gene 



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
        output_file_name = "OUT_" + str(input_document.get_filename())
        output_doc.document = os.path.join('users', str(input_document.project.owner),
                                            str(input_document.project),'output', output_file_name)
        output_doc.doc_type = 2
        output_doc.parameters = {'sigma_num': form.cleaned_data['sigma_num'],
                                 'use_sigma': form.cleaned_data['use_sigma'],
                                 'cnr_low': form.cleaned_data['cnr_low'],
                                 'cnr_up': form.cleaned_data['cnr_up'],
                                 'use_cnr': form.cleaned_data['use_cnr'] }
        output_doc.project = input_document.project
        output_doc.created_by = self.request.user
        output_doc.created_at = datetime.now()        
        output_doc.save()
        
        
        """ Calculating PMS and PMS1 """
         
        process_doc_df = read_csv(settings.MEDIA_ROOT+"/"+input_document.input_doc.document.name,
                                  sep='\t')
        
        process_doc_df = process_doc_df.set_index('SYMBOL') #create index by SYMBOL column
        
        tumour_columns = [col for col in process_doc_df.columns if 'Tumour' in col] #get 
        #output_columns = tumour_columns.append('Pathway')
        
        #output_pms_df = DataFrame(columns=output_columns) # dataframe to store PMS table
        #output_pms1_df = DataFrame(columns=output_columns) # dataframe to store PMS1 table
        
        out_list = []
        for pathway in Pathway.objects.all():
            gene_name = []
            gene_arr = []
            for gene in pathway.gene_set.all():
                gene_name.append(gene.name)
                gene_arr.append(gene.arr)
            
            gene_data = {'SYMBOL': gene_name,
                         'ARR': gene_arr}
            
            gene_df = DataFrame(gene_data)
            gene_df = gene_df.set_index('SYMBOL') #create index by SYMBOL column
            
            joined_df = gene_df.join(process_doc_df, how='inner')
            
            out_dict = {}
            out_dict['Pathway'] = pathway.name
            
            for tumour in tumour_columns: #loop thought samples columns
                
                summ = 0
                for index, row in joined_df.iterrows():
                    signum = 2
                    cnr_up = 1.5
                    cnr_low = 0.67
                    if (row[tumour]*row['Mean_norm'] > (row['Mean_norm']+signum*row['std']) or  \
                        row[tumour]*row['Mean_norm'] < (row['Mean_norm']-signum*row['std'])) and \
                       (row[tumour]>cnr_up or row[tumour]<cnr_low):
                        
                        summ+= float(row['ARR'])*math.log(row[tumour]) # calculate PMS'
                
                out_dict[tumour] = summ
            out_list.append(out_dict)
        
        
        output_pms_df = DataFrame(out_list)
                        
                    
            
             
        
        
       
        
        
        path = os.path.join('users', str(input_document.project.owner),
                                            str(input_document.project),'process', 'output_'+str(input_document.get_filename()))
        new_file = settings.MEDIA_ROOT+"/"+path
        
        path1 = os.path.join('users', str(input_document.project.owner),
                                            str(input_document.project),'process', 'join_'+str(input_document.get_filename()))
        new_file1 = settings.MEDIA_ROOT+"/"+path1
        
        joined_df.to_csv(new_file1, sep='\t', encoding='utf-8')
        
        
        
        output_pms_df.to_csv(new_file, sep='\t', encoding='utf-8')
        
        
        
        return HttpResponseRedirect(reverse('core_calculation', args=(output_doc.id,)))
    
        
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
        
