# -*- coding: utf-8 -*-
import logging

from django import forms
from django.forms.models import inlineformset_factory
from django.core.files.temp import NamedTemporaryFile

from django.contrib.auth.models import User
from profiles.models import Project, Document
from profiles.utils import validate_file

logger = logging.getLogger('oncoFinder')


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
        
class CalculationParametersForm(forms.Form):
    
    
    sigma_num = forms.FloatField( label="Sigma amount", initial=2, required=False)
    use_sigma = forms.BooleanField(label="Use sigma filter", initial=True, required=False)
    cnr_low = forms.FloatField(label="CNR lower limit", initial=0.67, required=False)
    cnr_up = forms.FloatField(label="CNR upper limit", initial=1.5, required=False)
    use_cnr = forms.BooleanField(label="Use CNR filter", initial=True, required=False)
    
    
    
    def __init__(self, *args, **kwargs):
        super(CalculationParametersForm, self).__init__(*args, **kwargs)
        self.fields['sigma_num'].widget.attrs.update({'class' : 'form-control input-sm'})
        self.fields['cnr_low'].widget.attrs.update({'class' : 'form-control input-sm'})
        self.fields['cnr_up'].widget.attrs.update({'class' : 'form-control input-sm'})