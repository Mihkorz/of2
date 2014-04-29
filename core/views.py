# -*- coding: utf-8 -*-
import os
from datetime import datetime
from pandas import read_csv

from django.views.generic.edit import FormView #CreateView , UpdateView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

from .forms import  CalculationParametersForm
from profiles.models import Document, ProcessDocument 



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
        
        """ Use PANDAS to preprocess input file(calculate Mean_norm and CNR) and save to process folder 
            Create ProcessDocument instance to store the file in database"""
            
        path = os.path.join('users', str(input_document.project.owner),
                                            str(input_document.project),'process', 'new_'+output_file_name)
        if not os.path.exists(settings.MEDIA_ROOT+'/'+os.path.join('users', str(input_document.project.owner),
                                            str(input_document.project),'process')):
            os.mkdir(settings.MEDIA_ROOT+'/'+os.path.join('users', str(input_document.project.owner),
                                            str(input_document.project),'process'))
        
        process_doc = ProcessDocument()
        process_doc.document = path
        process_doc.parameters = output_doc.parameters
        process_doc.input_doc = input_document
        process_doc.output_doc = output_doc
        process_doc.created_by = self.request.user
        process_doc.save()
        
        
        new_file = settings.MEDIA_ROOT+"/"+path
        
        df = read_csv(settings.MEDIA_ROOT+"/"+input_document.document.name, sep='\t')
        norm_cols = [col for col in df.columns if 'Norm' in col]
        tumour_cols = [col for col in df.columns if 'Tumour' in col]
        lTumors = {}
        for tumour in tumour_cols:
            lTumors[tumour+"_lvl"] = df[tumour]
            
        
        mean_norm = df[[norm for norm in norm_cols]].mean(axis=1)
        df['Mean_norm'] = mean_norm
        symbol_column = df['SYMBOL']
        df = df.drop('SYMBOL',1)
        
        df = df.div(df.Mean_norm, axis='index')
        df['SYMBOL'] = symbol_column
        df['Mean_norm'] = mean_norm
        for key in lTumors:
            df[key] = lTumors[key]
        df.to_csv(new_file, sep='\t', encoding='utf-8')
        
        
        return HttpResponseRedirect(reverse('core_calculation', args=(process_doc.id,)))
    
        
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
        
