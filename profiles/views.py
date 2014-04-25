# -*- coding: utf-8 -*-

#from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.conf import settings

from .forms import SettingsUserForm, UserProfileFormSet, CreateProjectForm, \
                   UploadDocumentForm
from .models import Project, Document

from pandas import read_csv


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
        
        all_projects = Project.objects.exclude(owner=self.get_object())
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
    
    
class ProjectDetail(DetailView):
    model = Project
    slug_field = "name"
    template_name = 'project/project_detail.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
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
        return super(CreateDocument, self).dispatch(request, *args, **kwargs)
        
    def form_valid(self, form):
        document = form.save(commit=False)
        project = form.cleaned_data['project']
        document.save()
        filename = settings.MEDIA_ROOT+"/"+document.document.name
        df = read_csv(filename, sep='\t')
        tumour_cols = [col for col in df.columns if 'Tumour' in col]
        norm_cols = [col for col in df.columns if 'Norm' in col]
        document.sample_num = len(tumour_cols)
        document.norm_num = len(norm_cols)
        document.row_num = len(df)
        document.save() 
        return HttpResponseRedirect(self.success_url+project.name)
        
    def form_invalid(self, form):
            return self.render_to_response(self.get_context_data(form=form))
        
class DocumentDetail(DetailView):
    model = Document
    template_name = "document/document_detail.html"
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DocumentDetail, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(DocumentDetail, self).get_context_data(**kwargs)
        filename = settings.MEDIA_ROOT+"/"+self.object.document.name 
        df = read_csv(filename, sep='\t')
        
        #tumor_cols = [col for col in df.columns if 'Nor' in col]
        
        context['test'] = df[:50].to_html()
        return context  
    