# -*- coding: utf-8 -*-
import logging

from django import forms
from django.forms.models import inlineformset_factory
from django.core.files.temp import NamedTemporaryFile
from .widgets import AdminImageWidget

from django.contrib.auth.models import User
from .models import Profile, Project, Document
from .utils import validate_file

logger = logging.getLogger('oncoFinder')

class SettingsUserForm(forms.ModelForm):
    class Meta(object):
        model = User
        exclude = ('last_login', 'password', 'is_superuser', 'username', 'is_staff', 
                   'is_active', 'date_joined', 'groups', 'user_permissions' )
         
class SettingsProfileForm(forms.ModelForm):
    class Meta(object):
        model = Profile
        exclude = ('location',)
        widgets = {'picture' : AdminImageWidget(),}
        
UserProfileFormSet = inlineformset_factory(User, Profile, form=SettingsProfileForm,
                                                   extra=1, can_delete=False)

class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'status']
        widgets = {'status': forms.RadioSelect()}
        
class UploadDocumentForm(forms.ModelForm):
    
    created_by = forms.ModelChoiceField(queryset=User.objects.all(),
            widget=forms.HiddenInput())
    project = forms.ModelChoiceField(queryset=Project.objects.all(),
            widget=forms.HiddenInput())
    
    def clean_document(self):
        try:
            uploaded_file = self.cleaned_data['document']
        
            temp_doc = NamedTemporaryFile(mode='w+', delete=True)
            temp_doc.write(uploaded_file.read())
            temp_doc.flush()
            temp_doc.seek(0)
            
            temp_doc._size = uploaded_file._size
            temp_doc._content_type = uploaded_file.content_type
            
            validate_file(temp_doc)
            
            temp_doc.close()            
  
        except forms.ValidationError:
            logger.error(u'User was trying to upload file with wrong format.')
            raise 

        return uploaded_file
    
    class Meta(object):
        model = Document
        fields = ['document', 'description', 'created_by', 'project', ]