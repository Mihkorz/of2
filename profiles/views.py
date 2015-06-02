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
from .preprocess_views import OfCnrPreprocess, IlluminaPreprocess, OfCnrStatPreprocess, \
                              MedicPreprocess
from core.stats import pseudo_ttest_1samp, fdr_corr
from core.models import Pathway, Component, Gene
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
        project = Project.objects.get(pk=request.POST.get('project', False))
        if project.field == 'med':
            view = MedicPreprocess.as_view()
            return view(request, *args, **kwargs)
             
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
                    context['PAS'] = df.to_html(classes=['pas_table', 'table', 'table-striped', 'table-bordered'])
                except:
                    try:
                        df = read_excel(filename, sheetname="PAS")
                        context['PAS'] = df.to_html(classes=['pas_table', 'table', 'table-striped', 'table-bordered'])
                    except:
                        pass
                try:
                    df = read_excel(filename, sheetname="PMS1")
                    context['PAS1'] = df.to_html(classes=['pas1_table', 'table', 'table-striped', 'table-bordered'])
                except:
                    try:
                        df = read_excel(filename, sheetname="PAS1")
                        context['PAS1'] = df.to_html(classes=['pas1_table', 'table', 'table-striped', 'table-bordered'])
                    except:
                        pass
                try:
                    df = read_excel(filename, sheetname="PMS2")
                    context['PAS2'] = df.to_html(classes=['pas2_table', 'table', 'table-striped', 'table-bordered'])
                except:
                    try:
                        df = read_excel(filename, sheetname="PAS2")
                        context['PAS2'] = df.to_html(classes=['pas2_table', 'table', 'table-striped', 'table-bordered'])
                    except:
                        pass
                try:
                    df = read_excel(filename, sheetname="DS1")
                    context['DS1'] = df.to_html(classes=['ds1_table', 'table', 'table-striped', 'table-bordered'])
                except:
                    try:
                        df = read_excel(filename, sheetname="DS1A")
                        context['DS1'] = df.to_html(classes=['ds1_table', 'table', 'table-striped', 'table-bordered'])
                    except:
                        pass
                try:
                    df = read_excel(filename, sheetname="DS2")
                    context['DS2'] = df.to_html(classes=['ds2_table', 'table', 'table-striped', 'table-bordered'])
                except:
                    pass
                try:
                    df = read_excel(filename, sheetname="DS1B")
                    context['DS1B'] = df.to_html(classes=['ds1b_table', 'table', 'table-striped', 'table-bordered'])
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
        
        out_fname = output_filename.split('/')[-1] 
        df_file_cnr = read_excel(settings.MEDIA_ROOT+"/users/"+self.object.project.owner.username+"/"+self.object.project.name+"/process/cnr_"+out_fname)
        
        df_cnr_raw = df_file_cnr[[sample, 'gMean_norm', 'std']]
        df_cnr_differential = df_cnr_raw[df_cnr_raw[sample]!=1]
        df_cnr_differential.columns = ['CNR', 'Mean norm', 'STD']
        context['genes'] = df_cnr_differential.to_html(classes=['gene_table', 'table', 'table-striped', 'table-bordered']) 
        #raise Exception('sample')
        
        context['path_db'] = calc_params['db']
        context['docpath'] = settings.MEDIA_ROOT+"/users/"+self.object.project.owner.username+"/"+self.object.project.name+"/process/cnr_"+out_fname
        context['sample_name'] = sample
        
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
                    if pathname != 'Pathway':
                        objPath = Pathway.objects.filter(name=pathname, organism=calc_params['organism'], database__in=calc_params['db'])[0]
                        objPath.pms = pms_values[0]
                        objPath.pms1 = pms_values[1]
                        lPaths.append(objPath)
                except:
                    raise
            
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
        
        pathway = Pathway.objects.get(pk = int(request.POST['pathway']))
        
        gene_objects = pathway.gene_set.all()
        gene_name = []
        gene_arr = []        
        for gene in gene_objects:
            gene_name.append(gene.name.strip().upper())
            gene_arr.append(float(gene.arr))
            
        gene_data = {'SYMBOL': gene_name,
                     'ARR': gene_arr}
   
            
        gene_df = DataFrame(gene_data).set_index('SYMBOL')
        
        sample = request.POST['sample_name']
        df_file_cnr = read_excel(request.POST['docpath'])
        
        df_cnr_raw = df_file_cnr[[sample, 'gMean_norm', 'std']]
        df_cnr_differential = df_cnr_raw[df_cnr_raw[sample]!=1]
        df_cnr_differential.columns = ['CNR', 'Mean norm', 'STD']
        df_cnr_differential.index.name = 'SYMBOL'
        
        joined_df = gene_df.join(df_cnr_differential, how='inner') #intersect DataFrames to acquire only genes in current pathway
        joined_df.reset_index(inplace=True)
        joined_df.index += 1
        context['joined'] = joined_df.to_html(classes=['table', 'table-bordered', 'table-striped'])
        context['diff_genes_count'] = len(joined_df.index)
        
        
        
        nComp = []
        dif_genes = {}
        for index, row in joined_df.iterrows():                
            
            loComp = Component.objects.filter(name = row['SYMBOL'], node__in=pathway.node_set.all())
            
            for comp in loComp:
                comp.cnr = row['CNR']
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
        
        
        context['diff_genes'] = dif_genes
           
        context['pathway'] = pathway
        
        return context  
    