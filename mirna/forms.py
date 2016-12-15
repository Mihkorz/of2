# -*- coding: utf-8 -*-
import logging

from django import forms
from django.forms.models import inlineformset_factory
from django.core.files.temp import NamedTemporaryFile
from django.contrib.auth.models import User

from core.models import PATHWAY_DATABASE, PATHWAY_ORGANISM
from mirna.models import MirnaDb
from profiles.models import Project, Document
from profiles.utils import validate_input_document

logger = logging.getLogger('oncoFinder')


class UploadDocumentForm(forms.ModelForm):
    
    created_by = forms.ModelChoiceField(queryset=User.objects.all(),
            widget=forms.HiddenInput())
    project = forms.ModelChoiceField(queryset=Project.objects.all(),
            widget=forms.HiddenInput())
    
    def clean_document(self):
        try:
            uploaded_file = self.cleaned_data['document']
            validate_input_document(uploaded_file)

        except forms.ValidationError:
            logger.error(u'User was trying to upload file with wrong format.')
            raise 

        return uploaded_file
    
    class Meta(object):
        model = Document
        fields = ['document', 'description', 'created_by', 'project', ]


class CalculationParametersForm(forms.Form):
    
    DB_CHOICES = MirnaDb.CHOISES

    ORGANISM_CHOICES = PATHWAY_ORGANISM

    PATH_DB_CHOICES = PATHWAY_DATABASE

    organism_choice = forms.ChoiceField(label="Organism",
                                     widget=forms.RadioSelect, choices=ORGANISM_CHOICES, initial='human')
    
    db_choice = forms.ChoiceField(label="Target DataBase",
                                     widget=forms.RadioSelect, choices=DB_CHOICES, initial=MirnaDb.MIRTARBASE_STRONG)
    path_db_choice = forms.MultipleChoiceField(label="Pathway DataBase",
                                     widget=forms.SelectMultiple, choices=PATH_DB_CHOICES, initial=['primary_old'])
    sigma_num = forms.FloatField( label="Sigma amount", initial=2, required=False)
    use_sigma = forms.BooleanField(label="Use sigma filter", initial=True, required=False)
    cnr_low = forms.FloatField(label="CNR lower limit", initial=0.67, required=False)
    cnr_up = forms.FloatField(label="CNR upper limit", initial=1.5, required=False)
    use_cnr = forms.BooleanField(label="Use CNR filter", initial=True, required=False)
    
    calculate_norms_pas = forms.BooleanField(label="PAS1 for Norms(requires at least 3 norms)", initial=True, required=False)
    
    
    def __init__(self, *args, **kwargs):
        super(CalculationParametersForm, self).__init__(*args, **kwargs)
        self.fields['sigma_num'].widget.attrs.update({'class' : 'form-control input-sm'})
        self.fields['cnr_low'].widget.attrs.update({'class' : 'form-control input-sm'})
        self.fields['cnr_up'].widget.attrs.update({'class' : 'form-control input-sm'})
