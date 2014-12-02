# -*- coding: utf-8 -*-
import os
import csv
import math
from datetime import datetime
from pandas import read_csv, read_excel, DataFrame, Series, ExcelWriter

from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView 
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

from .models import MirnaMapping
from .forms import UploadDocumentForm, CalculationParametersForm
from profiles.models import Project, Document
from database.models import Pathway, Gene

class mirnaProjectDetail(DetailView):
    model = Project
    slug_field = 'name'
    template_name = 'mirna/project_detail.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(mirnaProjectDetail, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(mirnaProjectDetail, self).get_context_data(**kwargs)
        context['form'] = UploadDocumentForm(initial={'created_by': self.request.user,
                                                      'project': self.object})
        context['documents'] = self.object.document_set.all() 
        
        
        
        
        return context
    
class mirnaDocumentDetail(DetailView):
    model = Document
    template_name = "mirna/document_detail.html"
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(mirnaDocumentDetail, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(mirnaDocumentDetail, self).get_context_data(**kwargs)
        
        filename = settings.MEDIA_ROOT+"/"+self.object.document.name 
        if self.object.doc_type == 1:
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(open(filename, 'r').read(), delimiters='\t,;') # defining the separator of the csv file
            df = read_csv(filename, delimiter=dialect.delimiter)
            context['input'] = df[:50].to_html()
        else:
            try:
                df = read_excel(filename, sheetname="miPAS")
                context['miPAS'] = df.to_html()
            except:
                pass
            try:
                df = read_excel(filename, sheetname="miPI")
                context['miPI'] = df.to_html()
            except:
                pass
        
        return context
    
class MirnaSetCalculationParameters(FormView):
    
    form_class = CalculationParametersForm
    template_name = 'mirna/mirna_calculation_parameters.html'
    success_url = '/success/'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):        
        return super(MirnaSetCalculationParameters, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(MirnaSetCalculationParameters, self).get_context_data(**kwargs)
        
        input_document = Document.objects.get(pk=self.kwargs['pk'])
        
        context['document'] = input_document
        
        
        return context
    
    def form_valid(self, form):
        sigma_num = form.cleaned_data['sigma_num']
        use_sigma = form.cleaned_data['use_sigma']
        cnr_low =  form.cleaned_data['cnr_low']
        cnr_up =  form.cleaned_data['cnr_up']
        use_cnr = form.cleaned_data['use_cnr']
        db_choice = form.cleaned_data['db_choice']
        
        
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
        json_db = db_choice
        output_doc.parameters = {'sigma_num': sigma_num,
                                 'use_sigma': use_sigma,
                                 'cnr_low': cnr_low,
                                 'cnr_up': cnr_up,
                                 'use_cnr': use_cnr,
                                 'db': json_db }
        output_doc.project = input_document.project
        output_doc.created_by = self.request.user
        output_doc.created_at = datetime.now()        
        #output_doc.save()
        
        """ Calculating miPAS and miRNA-Pathway Influence (miPI) """
         
        def strip(text):
            try:
                return text.strip()
            except AttributeError:
                return text
            
        process_doc_df = read_csv(settings.MEDIA_ROOT+"/"+input_document.input_doc.document.name,
                                  sep='\t', index_col='SYMBOL',  converters = {'SYMBOL' : strip}).fillna(0)        
        
        tumour_columns = [col for col in process_doc_df.columns if 'Tumour' in col] #get sample columns
        
        miPAS_list = []
        miPI_list = []
        
        pathway_objects = Pathway.objects.all()
        
        for pathway in pathway_objects:
            gene_name = []
            gene_arr = []
            
            gene_objects = pathway.gene_set.all()
            
            for gene in gene_objects:
                mapping_mirna_genes = MirnaMapping.objects.filter(Gene=gene.name, Sourse=db_choice)
                for mirna_gene in mapping_mirna_genes:
                    gene_name.append(mirna_gene.miRNA_ID.strip())
                    gene_arr.append(float(gene.arr))
                
            gene_data = {'SYMBOL': gene_name,
                         'ARR': gene_arr}
            
            gene_df = DataFrame(gene_data).set_index('SYMBOL')
            
            gene_df = gene_df.groupby(gene_df.index, level=0).mean() # ignore duplicate genes if exist 
            
            joined_df = gene_df.join(process_doc_df, how='inner')
            
            miPAS_dict = {}
            miPI_dict = {}
            
            miPAS_dict['Pathway'] = miPI_dict['Pathway'] = pathway.name.strip()
            
            for tumour in tumour_columns: #loop thought samples columns                
                summ = 0
                
                for index, row in joined_df.iterrows():
                    if not use_sigma:
                        sigma_num = 0
                    if not use_cnr:
                        cnr_up = cnr_low = 0
                    
                    
                    CNR = float(row[tumour])
                    try:
                        mean = float(row['gMean_norm'])
                    except:
                        mean = 0
                    EXPRESSION_LEVEL = CNR*float(mean)
                        
                    std = float(row['std']) if float(row['std'])>0 else 0   
                    if (
                        (
                           (EXPRESSION_LEVEL >= (mean + sigma_num*std)) or 
                           (EXPRESSION_LEVEL < (mean - sigma_num*std))
                         ) and 
                        (CNR > cnr_up or CNR < cnr_low) and 
                        (CNR > 0)
                       ):
                        
                        summ+= -1*float(row['ARR'])*math.log(CNR) # ARR*ln(CNR)
                        
            
                    
                miPAS_dict[tumour] = summ #miPAS
                miPI_dict[tumour] = float(pathway.amcf)*summ #miPI
                
            miPAS_list.append(miPAS_dict)
            miPI_list.append(miPI_dict)
            
            output_miPAS_df = DataFrame(miPAS_list)
            output_miPAS_df = output_miPAS_df.set_index('Pathway')
            output_miPI_df = DataFrame(miPI_list)
            output_miPI_df = output_miPI_df.set_index('Pathway')
            
        """ Saving results to Excel file and to database """
        path = os.path.join('users', str(input_document.project.owner),
                                            str(input_document.project),'output')
        file_name = 'output_'+str(input_document.get_filename()+'.xlsx')
        
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        
        output_file = default_storage.save(settings.MEDIA_ROOT+"/"+path+"/"+file_name, ContentFile(''))
        
        with ExcelWriter(output_file, index=False) as writer:
            output_miPAS_df.to_excel(writer,'miPAS')
            output_miPI_df.to_excel(writer,'miPI')
            
        output_doc.document = path+"/"+os.path.basename(output_file)
        output_doc.related_doc = input_document
        output_doc.save()        
        
        
        return HttpResponseRedirect(reverse('document_detail', args=(output_doc.id,)))
    
    def form_invalid(self, form):
            return self.render_to_response(self.get_context_data(form=form))

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

