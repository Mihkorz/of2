# -*- coding: utf-8 -*-

import os
import csv
import json
import math
import numpy as np
from pandas import read_csv, read_excel, DataFrame
from scipy.stats.mstats import gmean
from scipy.stats import ttest_1samp, ttest_ind, ranksums

#from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.models import User
from django.conf import settings

from .forms import SettingsUserForm, UserProfileFormSet, CreateProjectForm, \
                   UploadDocumentForm
from .models import Project, Document, ProcessDocument
from .preprocess_views import OfCnrPreprocess, IlluminaPreprocess, OfCnrStatPreprocess
from core.stats import pseudo_ttest_1samp, fdr_corr
from database.models import Pathway, Component, Gene
from mirna.views import mirnaProjectDetail, mirnaDocumentDetail


class ProfileIndex(DetailView):
    model = User
    slug_field = "username"
    context_object_name = "user_profile"
    template_name = "profiles/index.html"
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):        
        return super(ProfileIndex, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):              
        context = super(ProfileIndex, self).get_context_data(**kwargs)
        
        all_users = User.objects.exclude(username = self.get_object().username)
        context['all_users'] = all_users
        
        my_projects = Project.objects.filter(owner=self.get_object())
        context['my_projects'] = my_projects
        
        all_projects = Project.objects.exclude(owner=self.get_object())[:30]
        context['all_projects'] = all_projects
                
        return context
        
class SettingsProfile(UpdateView):
    model = User
    form_class = SettingsUserForm
    template_name = "profiles/settings_profile.html"
    success_url = "/settings/profile"
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):        
        return super(SettingsProfile, self).dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super(SettingsProfile, self).get_context_data(**kwargs)
        if self.request.POST:
            context['profile_form'] = UserProfileFormSet(self.request.POST, instance=self.object)
        else:
            context['profile_form'] = UserProfileFormSet(instance=self.object)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        profile_form = context['profile_form']
        
        if profile_form.is_valid():
            self.object = form.save()
            profile_form.instance = self.object
            profile_form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))
        
    def form_invalid(self, form):
            return self.render_to_response(self.get_context_data(form=form))
    
class SettingsBilling(UpdateView):
    pass

class CreateProject(CreateView):
    form_class = CreateProjectForm
    template_name = 'project/project_create.html'
    success_url = '/project/'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateProject, self).dispatch(request, *args, **kwargs)
        
    def form_valid(self, form):
        project = form.save(commit=False)
        project.owner = self.request.user
        project.name = slugify(form.cleaned_data['name'])
        project.save()
        return HttpResponseRedirect(self.success_url+project.name)
        
    def form_invalid(self, form):
            return self.render_to_response(self.get_context_data(form=form))
    
class DeleteProject(DeleteView):
    model = Project
    template_name = 'project/project_confirm_delete.html'
    success_url = '/'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        # maybe do some checks here for permissions ...

        resp = super(DeleteProject, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data),
                content_type="application/json")
        else:
            # POST request (not ajax) will do a redirect to success_url
            return resp
        
    def get_object(self, queryset=None):
        """ Hook to ensure project is owned by request.user. """
        obj = super(DeleteProject, self).get_object()
        if not obj.owner == self.request.user:
            raise Http404
        return obj

    
class ProjectDetail(DetailView):
    model = Project
    slug_field = "name"
    template_name = 'project/project_detail.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().field == 'rna':
            view=mirnaProjectDetail.as_view()
            return view( request, *args, **kwargs )
        return super(ProjectDetail, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        context['form'] = UploadDocumentForm(initial={'created_by': self.request.user,
                                                      'project': self.object})
        context['documents'] = self.object.document_set.all()
        return context

class CreateDocument(CreateView): 
    form_class = UploadDocumentForm
    template_name = 'document/document_create.html'
    success_url = '/project/'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        doc_format = request.POST.get('doc_format', False)
        if doc_format == 'OF_cnr':
            view = OfCnrPreprocess.as_view()
            return view(request, *args, **kwargs)
        if doc_format == 'OF_cnr_stat':
            view = OfCnrStatPreprocess.as_view()
            return view(request, *args, **kwargs)
        if doc_format == 'Illumina':
            view = IlluminaPreprocess.as_view()
            return view(request, *args, **kwargs)
        return super(CreateDocument, self).dispatch(request, *args, **kwargs)
        
    def form_valid(self, form):
        document = form.save(commit=False)
        project = form.cleaned_data['project']
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
        document.save()
        
        """ Use PANDAS to preprocess input file(calculate Mean_norm CNR and STD) and save to process folder 
            Create ProcessDocument instance to store the file in database"""
            
        path = os.path.join('users', str(document.project.owner),
                                            str(document.project),'process', 'process_'+str(document.get_filename()))
        if not os.path.exists(settings.MEDIA_ROOT+'/'+os.path.join('users', str(document.project.owner),
                                            str(document.project),'process')):
            os.mkdir(settings.MEDIA_ROOT+'/'+os.path.join('users', str(document.project.owner),
                                            str(document.project),'process'))
        
        process_doc = ProcessDocument()
        process_doc.document = path
        process_doc.input_doc = document
        process_doc.created_by = self.request.user
        process_doc.save()
        
        new_file = settings.MEDIA_ROOT+"/"+path
        
                
        df = df.set_index('SYMBOL') #create index by SYMBOL column
        
        
        if project.field == 'rna':
         
            df = df.groupby(df.index, level=0).mean() #deal with duplicate genes by taking mean value
        
            mean_norm = df[[norm for norm in norm_cols]].mean(axis=1)
            from scipy.stats.mstats import gmean
            gmean_norm = df[[norm for norm in norm_cols]].apply(gmean, axis=1)
        
            df1 = DataFrame(df[[norm for norm in norm_cols]], index=df.index)
        
            df1 = df1.std(axis=1)
                
            df['Mean_norm'] = mean_norm
            df['gMean_norm'] = gmean_norm
            
            df[df['Mean_norm'] == 0] = 1
               
            df = df.div(df.Mean_norm, axis='index')
       
            df['Mean_norm'] = mean_norm
            df['gMean_norm'] = gmean_norm
            df['std'] = df1
            df = df.fillna(0)    
        
            
        if project.field == 'med':
            
            if len(tumour_cols) > 1:
                from django import forms 
                raise forms.ValidationError(u"There is more than one patient in the file!")                 
                
    
        df.to_csv(new_file, sep='\t')
         
        return HttpResponseRedirect(self.success_url+project.name)
        
    def form_invalid(self, form):
            return self.render_to_response(self.get_context_data(form=form))


class DeleteDocument(DeleteView):
    model = Document
    template_name = 'document/document_confirm_delete.html'
    success_url = '/'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        # maybe do some checks here for permissions ...

        resp = super(DeleteDocument, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data),
                content_type="application/json")
        else:
            # POST request (not ajax) will do a redirect to success_url
            return resp
        
    def get_object(self, queryset=None):
        """ Make some additional filtering with object """
        obj = super(DeleteDocument, self).get_object()
        #if not obj.owner == self.request.user:
        #    raise Http404
        return obj
        
class DocumentDetail(DetailView):
    
    
    model = Document
    template_name = "document/document_detail.html"
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().project.field == 'rna':
            view=mirnaDocumentDetail.as_view()
            return view( request, *args, **kwargs )
        return super(DocumentDetail, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(DocumentDetail, self).get_context_data(**kwargs)
        
        filename = settings.MEDIA_ROOT+"/"+self.object.document.name 
        if self.object.doc_type == 1:
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(open(filename, 'r').read(), delimiters='\t,;') # defining the separator of the csv file
            df = read_csv(filename, delimiter=dialect.delimiter)
            context['input'] = df[:50].to_html()            
        else:
            if self.object.project.field == 'sci':
                try:
                    df = read_excel(filename, sheetname="PMS")
                    context['PAS'] = df.to_html()
                except:
                    try:
                        df = read_excel(filename, sheetname="PAS")
                        context['PAS'] = df.to_html()
                    except:
                        pass
                try:
                    df = read_excel(filename, sheetname="PMS1")
                    context['PAS1'] = df.to_html()
                except:
                    try:
                        df = read_excel(filename, sheetname="PAS1")
                        context['PAS1'] = df.to_html()
                    except:
                        pass
                try:
                    df = read_excel(filename, sheetname="PMS2")
                    context['PAS2'] = df.to_html()
                except:
                    try:
                        df = read_excel(filename, sheetname="PAS2")
                        context['PAS2'] = df.to_html()
                    except:
                        pass
                try:
                    df = read_excel(filename, sheetname="DS1")
                    context['DS1'] = df.to_html()
                except:
                    try:
                        df = read_excel(filename, sheetname="DS1A")
                        context['DS1'] = df.to_html()
                    except:
                        pass
                try:
                    df = read_excel(filename, sheetname="DS2")
                    context['DS2'] = df.to_html()
                except:
                    pass
                try:
                    df = read_excel(filename, sheetname="DS1B")
                    context['DS1B'] = df.to_html()
                except:
                    pass
            
                tumour_cols = [col for col in df.columns if 'Tumour' in col]
                context['tumour_cols'] = tumour_cols
            
            """ MEDIC OUTPUT FILE """
            if self.object.project.field == 'med':
            
                self.template_name = "document/medic_doc_detail.html"
                from medic.models import TreatmentMethod
                treatments = TreatmentMethod.objects.filter(nosology=self.object.project.nosology)
                
                hormone_status = self.object.parameters['hormone_status']
                her2_status = self.object.parameters['her2_status']
                
                if hormone_status!='0':
                    treatments = treatments.filter(hormone_receptor_status=hormone_status)
                    
                if her2_status!='0':
                    treatments = treatments.filter(her2_status=her2_status)
                    
                
                context['treatments'] = treatments
                
                
        return context
    
class SampleDetail(DeleteView):
    """
    Details for current Sample
    """
    model = Document
    template_name = 'document/sample_detail.html'
    
    
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SampleDetail, self).dispatch(request, *args, **kwargs)
        
    
    def get_context_data(self, **kwargs):
        context = super(SampleDetail, self).get_context_data(**kwargs)
        
        sample = self.kwargs['sample_name']
        errors = []
        
        output_filename = settings.MEDIA_ROOT+"/"+self.object.document.name
        process_filename = settings.MEDIA_ROOT+"/"+self.object.related_doc.input_doc.document.name
        calc_params = self.object.parameters
        
        context['path_db'] = calc_params['db']
        
        def strip(text):
            try:
                return text.strip().upper()
            except AttributeError:
                return text
        
        try: # searching for differential genes once again. Don't forget to change in case of main calculation filter changes!
            process_doc_df = read_csv(settings.MEDIA_ROOT+"/"+self.object.related_doc.input_doc.document.name,
                                  sep='\t', index_col='SYMBOL',  converters = {'SYMBOL' : strip}).fillna(0)
            
            norms_doc_df = process_doc_df[[norm for norm in [col for col in process_doc_df.columns if 'Norm' in col]]]
            cnr_mean_norm =  norms_doc_df.mean(axis=1)        
            cnr_gMean_norm = norms_doc_df.apply(gmean, axis=1)
            std=norms_doc_df.std(axis=1) # standard deviation
            if calc_params['norm_algirothm']=='geometric': #geometric norms
                divide = cnr_gMean_norm
            else:             #arithmetic norms
                divide = cnr_mean_norm  
    
            process_doc_df = process_doc_df.div(divide, axis='index')
        
            process_doc_df['Mean_norm'] = cnr_mean_norm
            process_doc_df['gMean_norm'] = cnr_gMean_norm
            process_doc_df['std'] = std
            
            if calc_params['use_ttest']:
                def calculate_ttest(row):
                    tumours = row[[t for t in row.index if 'Tumour' in t]]
                    norms = row[[n for n in row.index if 'Norm' in n]]
                       
                    _, p_val = ttest_ind(tumours, norms)
            
                    return p_val
                
                log_process_doc_df = np.log(process_doc_df).fillna(0)
                series_p_values = log_process_doc_df.apply(calculate_ttest, axis=1).fillna(0)
                process_doc_df['p_value'] = series_p_values
                if calc_params['use_fdr']:
                    fdr_q_values = fdr_corr(np.array(series_p_values))
                    fdr_df = DataFrame({'p' : series_p_values,
                                        'q' : fdr_q_values
                                       })
                    process_doc_df['q_value'] = fdr_df['q']
                    process_doc_df = process_doc_df[process_doc_df['q_value']<0.05]
                else:
                    process_doc_df = process_doc_df[process_doc_df['p_value']<0.05]
            
            df_genes = process_doc_df[[sample, 'Mean_norm', 'gMean_norm', 'std']]
            
            #raise Exception('yo')
            
            
            diff_genes_for_sample = []
            dict_diff_genes_for_sample = {}
            for gene_name, row in df_genes.iterrows():
                if not calc_params['use_sigma']:
                    sigma_num = 0
                else:
                    sigma_num = calc_params['sigma_num']
                if not calc_params['use_cnr']:
                    cnr_up = cnr_low = 0
                else:
                    cnr_up = calc_params['cnr_up']
                    cnr_low = calc_params['cnr_low']
                        
                CNR = row[sample]
                if calc_params['norm_algirothm'] == 'arithmetic':
                    mean = row['Mean_norm']
                    column_name = 'Mean_norm'
                    EXPRESSION_LEVEL = CNR*float(mean)
                         
                if calc_params['norm_algirothm'] == 'geometric':
                    mean = row['gMean_norm']
                    column_name = 'gMean_norm'
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
                        
                    diff_genes_for_sample.append(gene_name) # store differential genes in a list
                    dict_diff_genes_for_sample[gene_name] = CNR # dictionary gene_name: CNR for Show Details window
            
            dict_diff_genes = {'SYMBOL': diff_genes_for_sample}
            
            dif_genes_df = DataFrame(dict_diff_genes)
            dif_genes_df = dif_genes_df.set_index('SYMBOL')
            
            joined_df = dif_genes_df.join(df_genes, how='inner')
            
            joined_df = joined_df[[sample, column_name, 'std']]
            joined_df.columns =  ['CNR', 'Mean norm', 'STD']
            
            dict_genes = joined_df.to_dict(outtype="dict")
            
            output_genes = {}
            
            for gene in dict_genes['CNR']:
                output_genes[gene] = [d[gene] for d in (dict_genes['CNR'], dict_genes['Mean norm'], dict_genes['STD'])] 
            
            context['json_diff_genes'] = json.dumps(dict_diff_genes_for_sample) 
            context['genes'] = output_genes   
        except:
            errors.append("Error while determining differential genes!")
        
        try: # reading data from file
            df_file_pms = read_excel(output_filename, sheetname="PAS")
            df_file_pms1 = read_excel(output_filename, sheetname="PAS1")
            
        except:
            errors.append("Error reading PAS from File!")
        
        try:
            df_file_ds1 = read_excel(output_filename, sheetname="DS1")
            df_file_ds2 =  read_excel(output_filename, sheetname="DS2")
        except:
            errors.append("Error reading Drug Scores!")
        
        try:
            df_pms = df_file_pms[[sample]]
            df_pms.columns = ['PAS']
            
            pms_dict =  df_pms.to_dict(outtype="dict")
        except:
            pms_dict = {}
                
        
        try: # constructing PMS dictionary for displaying
            
            
            df_pms1 = df_file_pms1[[sample]]
            df_pms1.columns = ['PAS1']
            pms1_dict =  df_pms1.to_dict(outtype="dict")
            #pms_dict['PAS1'] = df_pms1.to_dict(outtype="dict")
            output_pms = {}
            
            for path in pms_dict['PAS']:
                output_pms[path] = [d[path] for d in (pms_dict['PAS'], pms1_dict['PAS1'])]
                
            # drawing Normal-Cancer cell picture 
            lPaths = []
            for pathname, pms_values in output_pms.iteritems():
                try:
                    objPath = Pathway.objects.get(name=pathname)
                    objPath.pms = pms_values[0]
                    objPath.pms1 = pms_values[1]
                    lPaths.append(objPath)
                except:
                    pass
            
            lUp = []
            lDown = []
            lCenter = []
            lDrawCanvas = []
            lDrawSVG = []
            
            for pathway in lPaths:
                if((pathway.amcf == -1 and pathway.pms1 <0) or (pathway.amcf == 1 and pathway.pms1 >0)):
                    lUp.append(pathway)
                elif((pathway.amcf == -1 and pathway.pms1 >0) or (pathway.amcf == 1 and pathway.pms1 <0)):
                    lDown.append(pathway)
                elif(pathway.pms == 0):
                    lCenter.append(pathway)
                    
            
            up = 0
            sortUp = sorted(lUp, key=lambda x: x.pms, reverse=True)
            sortUpR = sortUp[:10]
            sortUpR.reverse()
            for path in sortUpR:
                if path.pms1 >0:
                    color = "green"
                else:
                    color = "red"
                if path.amcf ==1:
                    markerSVG = 'marker-mid="url(#arrow)"'
                    markerCanvas = 'triangle'
                else:
                    markerSVG = 'marker-mid="url(#box)"'
                    markerCanvas = 'rect'
                
                height = 160-up*25
                thickness = 1*math.log(math.fabs(path.pms))
                lDrawSVG.append('<path id = "pathup'+str(path.id)+'" d = "M 200 200 Q 362,'+str(height)+'  525, '+str(height)+' Q 688,'+str(height)+' 850,200" \
                                 '+ markerSVG +' stroke = "'+ color +'" stroke-width = "'+str(thickness)+'" fill = "none"  />\
                                 <text x="10" y="100" style="stroke: #000000; font-size: 9pt; cursor: pointer" onclick="showDialog('+str(path.id)+')">\
                                 <textPath xlink:href="#pathup'+str(path.id)+'" startOffset="25%" >\
                                '+ path.name +'\
                                </textPath>\
                                </text>')
            
                canvasY = 270 - up*30+20
                lDrawCanvas.append('drawLink(200,'+str(canvasY)+',"'+ path.name +'", "'+ str(path.id) +'", "'+color+'", '+str(thickness)+', "'+markerCanvas+'");')
            
                up+=1
        
            down = 0
            sortDown = sorted(lDown, key=lambda x: x.pms, reverse=False)
            sortDownR = sortDown[:10]
            sortDownR.reverse()
            for path in sortDownR:
                if path.pms1 >0:
                    color = "green"
                else:
                    color = "red"
                if path.amcf ==1:
                    markerSVG = 'marker-mid="url(#arrow)"'
                    markerCanvas = 'triangle'
                else:
                    markerSVG = 'marker-mid="url(#box)"'
                    markerCanvas = 'rect'
                height = 250+down*25
                thickness = 1*math.log(math.fabs(path.pms))
                lDrawSVG.append('<path id = "pathdown'+str(down)+'"    d = "M 200 200 Q 362,'+str(height)+'  525, '+str(height)+' Q 688,'+str(height)+' 850,200" \
                                '+ markerSVG +' stroke = "'+ color +'" stroke-width = "'+str(thickness)+'" fill = "none"/>\
                                <text x="10" y="100" style="stroke: #000000; font-size: 9pt;cursor: pointer" onclick="showDialog('+str(path.id)+')">\
                                 <textPath xlink:href="#pathdown'+str(down)+'" startOffset="25%" >\
                                '+ path.name +'\
                                </textPath>\
                                </text>')
            
                canvasY = 410 + down*30
                lDrawCanvas.append('drawLink(200,'+str(canvasY)+',"'+ path.name +'", "'+ str(path.id) +'", "'+color+'", '+str(thickness)+', "'+markerCanvas+'");')
            
                down+=1
        
            for path in lCenter:
                if path.pms1 >= 0:
                    color = "green"
                else:
                    color = "red"
            
                           
            context['PMS'] = lPaths
            context['lDrawPathCanvas'] = lDrawCanvas

        except:
            raise
            errors.append("Error processing PMS and PMS1 DataFrames!")
            
        try: # constructing DS dictionary for displaying
            df_ds1 = df_file_ds1[[sample, 'DataBase']]
            df_ds1.columns = ['DS1', 'DataBase']
            df_ds2 = df_file_ds2[[sample]]
            df_ds2.columns = ['DS2']
            df_ds1 = df_ds1.join(df_ds2, how="inner")
            ds_dict =  df_ds1.to_dict(outtype="dict")
            
            output_ds = {}
            for drug in ds_dict['DS1']:
                output_ds[drug] = [d[drug] for d in (ds_dict['DataBase'], ds_dict['DS1'], ds_dict['DS2'] )]
            
            context['DS'] = output_ds
        except:
            errors.append("Error processing DS and DS2 DataFrames!")     
        
        context['error'] = errors
        context['sample_name'] = self.kwargs['sample_name']
        
        return context
    
class AjaxPathDetail(TemplateView):
    template_name = 'document/ajax_pathway_detail.html'
    
    def post(self, request, **kwargs):
        return self.render_to_response(self.get_context_data( request, **kwargs), **kwargs)
    
    
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxPathDetail, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, request, **kwargs):
        context = super(AjaxPathDetail, self).get_context_data(**kwargs)
        
        #path_db = request.POST['path_db']
        
        pathway = Pathway.objects.get(pk = int(request.POST['pathway']))
        dDifGenes = json.loads(request.POST['jsonGenes'])
        
        
        nComp = []
        dif_genes = {}
        for gName, gCnr in dDifGenes.iteritems():
            
            try:
                gene = Gene.objects.get(name = gName, pathway = pathway)
                dif_genes[gName] = [gCnr, gene.arr]
            except:
                pass
                
            
            loComp = Component.objects.filter(name = gName)
            
            for comp in loComp:
                if comp.node in pathway.node_set.all():
                    comp.cnr = gCnr
                    nComp.append(comp)
                    
        lNodes = []
        
        for node in pathway.node_set.all():
            node.nel = 0.0
            node.numDiffComp = 0
            node.sumDiffComp = 0.0
            node.color = "grey"
            node.strokeWidth = 1
            for component in nComp:
                if component in node.component_set.all():
                    if component.cnr != 0:
                        node.numDiffComp += 1
                        node.sumDiffComp += float(component.cnr)
            if node.numDiffComp >0 :
                node.nel = node.sumDiffComp / node.numDiffComp
            lNodes.append(node)
        
        
               
        
        finalNodes = []
        for nod in lNodes:
            if nod.nel > 1:
                nod.color = "green"
                nod.strokeWidth = math.log(nod.nel, 2)
            if nod.nel <= 1 and nod.nel > 0:
                nod.color = "red"
                nod.strokeWidth = math.log(nod.nel, 2)
            finalNodes.append(nod)            
        
        context['colorNodes'] = finalNodes   
        
              
        
        dRelations = []
        for node in pathway.node_set.all():
            for inrel in node.inrelations.all():
                relColor = 'black'
                if inrel.reltype == '1':
                    relColor = 'green'
                if inrel.reltype == '0':
                    relColor = 'red'
                dRelations.append({ inrel.fromnode.name : [inrel.tonode.name, relColor] })      
        context['dRelations'] = dRelations 
        
        context['pathway'] = pathway
        context['diff_genes'] = dif_genes
           
        
        
        return context  
    