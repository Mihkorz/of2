# -*- coding: utf-8 -*-

import os
import csv
import json
import math
from pandas import read_csv, read_excel, DataFrame

from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from .forms import SettingsUserForm, UserProfileFormSet, CreateProjectForm, \
                   UploadDocumentForm
from .models import Project, Document, ProcessDocument, IlluminaProbeTarget

from database.models import Pathway, Component, Gene


class OfCnrPreprocess(FormView):
    
    form_class = UploadDocumentForm
    template_name = 'document/document_create.html'
    success_url = '/project/'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(OfCnrPreprocess, self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        document = form.save(commit=False)
        document.save()
        filename = settings.MEDIA_ROOT+"/"+document.document.name
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(open(filename, 'r').read(), delimiters='\t,;') # defining the separator of the csv file
        df = read_csv(filename, delimiter=dialect.delimiter)
        tumour_cols = [col for col in df.columns if 'Tumour' in col]
        norm_cols = [col for col in df.columns if 'Norm' in col]
        document.sample_num = len(tumour_cols)
        document.norm_num = len(norm_cols)
        document.row_num = len(df)
        document.doc_format = 'OF_cnr'
        document.save()
        
        path = os.path.join('users', str(document.project.owner),
                                            str(document.project),'process', 'process_'+str(document.get_filename()))
        if not os.path.exists(settings.MEDIA_ROOT+'/'+os.path.join('users', str(document.project.owner),
                                            str(document.project),'process')):
            os.mkdir(settings.MEDIA_ROOT+'/'+os.path.join('users', str(document.project.owner),
                                            str(document.project),'process'))
        new_file = settings.MEDIA_ROOT+"/"+path
         
        process_doc = ProcessDocument()
        process_doc.document = path
        process_doc.input_doc = document
        process_doc.created_by = self.request.user
        process_doc.save()
        
        df.to_csv(new_file, sep='\t')
        
        return HttpResponseRedirect(self.success_url+document.project.name)
    
    
    def form_invalid(self, form):
            return self.render_to_response(self.get_context_data(form=form))
    
    
class IlluminaPreprocess(FormView):
    
    form_class = UploadDocumentForm
    template_name = 'document/document_create.html'
    success_url = '/project/'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(IlluminaPreprocess, self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        document = form.save(commit=False)
        project = form.cleaned_data['project']
        document.save()
        filename = settings.MEDIA_ROOT+"/"+document.document.name
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(open(filename, 'r').read(), delimiters='\t,;') # defining the separator of the csv file
        
        def strip(text):
            try:
                return text.strip().upper()
            except AttributeError:
                return text
        
        
        df1 = read_csv(filename, delimiter=dialect.delimiter,
                        converters = {'SYMBOL' : strip}).fillna(0) 
        
        
        probetargets = IlluminaProbeTarget.objects.all()
        mapping_dict = {}
        for probetarget in probetargets:
            mapping_dict[probetarget.PROBE_ID] = probetarget.TargetID
            
        dfff = df1['SYMBOL'].map(mapping_dict, na_action='ignore')
        
        """
        for row in columns:
            try:
                probetarget = IlluminaProbeTarget.objects.get(PROBE_ID=row['SYMBOL'])
                genes.append(probetarget.TargetID)
            except ObjectDoesNotExist:
                genes.append(row['SYMBOL'])
        """
        raise Exception('exception')
        return HttpResponseRedirect(self.success_url+document.project.name)
    
    def form_invalid(self, form):
            return self.render_to_response(self.get_context_data(form=form))    
    
    
    
    
    
    
    
    
    
    
    