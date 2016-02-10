# -*- coding: utf-8 -*-
import os
import pandas as pd
import subprocess

from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django import forms
from django.conf import settings
from django.shortcuts import redirect

class nnBloodForm(forms.Form):
    Alpha_amylase = forms.FloatField( label="Alpha-amylase", initial=0, required=False, help_text='Extreme Range here')
    ESR = forms.FloatField( label="ESR (by Westergren)", initial=0, required=False, help_text='Extreme Range here')
    Bilirubin_total = forms.FloatField( label="Bilirubin total", initial=0, required=False, help_text='Extreme Range here')
    Bilirubin_direct = forms.FloatField( label="Bilirubin direct", initial=0, required=False, help_text='Extreme Range here')
    Gamma_GT = forms.FloatField( label="Gamma-GT", initial=0, required=False, help_text='Extreme Range here')
    Glucose = forms.FloatField( label="Glucose", initial=0, required=False, help_text='Extreme Range here')
    Creatinine = forms.FloatField( label="Creatinine", initial=0, required=False, help_text='Extreme Range here')
    Lactate_dehydrogenase = forms.FloatField( label="Lactate dehydrogenase", initial=0, required=False, help_text='Extreme Range here')
    Urea = forms.FloatField( label="Urea", initial=0, required=False, help_text='Extreme Range here')
    Protein_total = forms.FloatField( label="Protein total", initial=0, required=False, help_text='Extreme Range here')
    Alpha_1_globulins = forms.FloatField( label="Alpha-1-globulins", initial=0, required=False, help_text='Extreme Range here')
    Alpha_1_globulins1 = forms.FloatField( label="Alpha-1-globulins", initial=0, required=False, help_text='Extreme Range here')
    Beta_globulins = forms.FloatField( label="Beta-globulins", initial=0, required=False, help_text='Extreme Range here')
    Gamma_globulins = forms.FloatField( label="Gamma-globulins", initial=0, required=False, help_text='Extreme Range here')
    Triglycerides = forms.FloatField( label="Triglycerides", initial=0, required=False, help_text='Extreme Range here')
    Cholesterol = forms.FloatField( label="Cholesterol", initial=0, required=False, help_text='Extreme Range here')
    HDL_Cholesterol = forms.FloatField( label="HDL Cholesterol", initial=0, required=False, help_text='Extreme Range here')
    LDL_cholesterol = forms.FloatField( label="LDL cholesterol (by Friedewald)", initial=0, required=False, help_text='Extreme Range here')
    Alkaline_phosphatase = forms.FloatField( label="Alkaline phosphatase", initial=0, required=False, help_text='Extreme Range here')
    Calcium = forms.FloatField( label="Calcium", initial=0, required=False, help_text='Extreme Range here')
    Chlorine = forms.FloatField( label="Chlorine", initial=0, required=False, help_text='Extreme Range here')
    Potassium = forms.FloatField( label="Potassium", initial=0, required=False, help_text='Extreme Range here')
    Sodium = forms.FloatField( label="Sodium", initial=0, required=False, help_text='Extreme Range here')
    Iron = forms.FloatField( label="Iron", initial=0, required=False, help_text='Extreme Range here')
    Hemoglobin = forms.FloatField( label="Hemoglobin", initial=0, required=False, help_text='Extreme Range here')
    Hematocrit = forms.FloatField( label="Hematocrit", initial=0, required=False, help_text='Extreme Range here')
    MCH = forms.FloatField( label="MCH", initial=0, required=False, help_text='Extreme Range here')
    MCHC = forms.FloatField( label="MCHC", initial=0, required=False, help_text='Extreme Range here')
    MCV = forms.FloatField( label="MCV", initial=0, required=False, help_text='Extreme Range here')
    Platelets = forms.FloatField( label="Platelets", initial=0, required=False, help_text='Extreme Range here')
    Erythrocytes = forms.FloatField( label="Erythrocytes", initial=0, required=False, help_text='Extreme Range here')
    Leukocytes = forms.FloatField( label="Leukocytes", initial=0, required=False, help_text='Extreme Range here')
    ALT = forms.FloatField( label="ALT", initial=0, required=False, help_text='Extreme Range here')
    AST = forms.FloatField( label="AST", initial=0, required=False, help_text='Extreme Range here')
    Albumen = forms.FloatField( label="Albumen", initial=0, required=False, help_text='Extreme Range here')
    Basophils = forms.FloatField( label="Basophils, %", initial=0, required=False, help_text='Extreme Range here')
    Eosinophils = forms.FloatField( label="Eosinophils, %", initial=0, required=False, help_text='Extreme Range here')
    Lymphocytes = forms.FloatField( label="Lymphocytes, %", initial=0, required=False, help_text='Extreme Range here')
    Monocytes = forms.FloatField( label="Monocytes, %", initial=0, required=False, help_text='Extreme Range here')
    NEUT = forms.FloatField( label="NEUT", initial=0, required=False, help_text='Extreme Range here')
    RDW = forms.FloatField( label="RDW", initial=0, required=False, help_text='Extreme Range here')
   
    
class nnBloodView(FormView):
    template_name = 'website/nn_blood.html'
    form_class = nnBloodForm
    success_url = 'result/'
    
    
    def dispatch(self, request, *args, **kwargs):      
        return super(nnBloodView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(nnBloodView, self).get_context_data(**kwargs)
        
        
                
        context['document'] = 'input_document'
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        
        df = pd.DataFrame()
        
        df.loc[:,'Alpha-amylase'] = pd.Series(form.cleaned_data['Alpha_amylase'])
        df.loc[:,'ESR (by Westergren)'] = pd.Series(form.cleaned_data['ESR'])
        df.loc[:,'Bilirubin total'] = pd.Series(form.cleaned_data['Bilirubin_total'])
        df.loc[:,'Bilirubin direct'] = pd.Series(form.cleaned_data['Bilirubin_direct'])
        df.loc[:,'Gamma-GT'] = pd.Series(form.cleaned_data['Gamma_GT'])
        df.loc[:,'Glucose'] = pd.Series(form.cleaned_data['Glucose'])
        df.loc[:,'Creatinine'] = pd.Series(form.cleaned_data['Creatinine'])
        df.loc[:,'Lactate dehydrogenase'] = pd.Series(form.cleaned_data['Lactate_dehydrogenase'])
        df.loc[:,'Urea'] = pd.Series(form.cleaned_data['Urea'])
        df.loc[:,'Protein total'] = pd.Series(form.cleaned_data['Protein_total'])
        
        df.loc[:,'Alpha-1-globulins'] = pd.Series(form.cleaned_data['Alpha_1_globulins'])
        df.loc[:,'Alpha-1-globulins1'] = pd.Series(form.cleaned_data['Alpha_1_globulins1'])
        df.loc[:,'Beta-globulins'] = pd.Series(form.cleaned_data['Beta_globulins'])
        df.loc[:,'Gamma-globulins'] = pd.Series(form.cleaned_data['Gamma_globulins'])
        df.loc[:,'Triglycerides'] = pd.Series(form.cleaned_data['Triglycerides'])
        df.loc[:,'Cholesterol'] = pd.Series(form.cleaned_data['Cholesterol'])
        df.loc[:,'HDL Cholesterol'] = pd.Series(form.cleaned_data['HDL_Cholesterol'])
        df.loc[:,'LDL cholesterol (by Friedewald)'] = pd.Series(form.cleaned_data['LDL_cholesterol'])
        df.loc[:,'Alkaline phosphatase'] = pd.Series(form.cleaned_data['Alkaline_phosphatase'])
        df.loc[:,'Calcium'] = pd.Series(form.cleaned_data['Calcium'])
        
        df.loc[:,'Chlorine'] = pd.Series(form.cleaned_data['Chlorine'])
        df.loc[:,'Potassium'] = pd.Series(form.cleaned_data['Potassium'])
        df.loc[:,'Sodium'] = pd.Series(form.cleaned_data['Sodium'])
        df.loc[:,'Iron'] = pd.Series(form.cleaned_data['Iron'])
        df.loc[:,'Hemoglobin'] = pd.Series(form.cleaned_data['Hemoglobin'])
        df.loc[:,'Hematocrit'] = pd.Series(form.cleaned_data['Hematocrit'])
        df.loc[:,'MCH'] = pd.Series(form.cleaned_data['MCH'])
        df.loc[:,'MCHC'] = pd.Series(form.cleaned_data['MCHC'])
        df.loc[:,'MCV'] = pd.Series(form.cleaned_data['MCV'])
        df.loc[:,'Platelets'] = pd.Series(form.cleaned_data['Platelets'])
        
        df.loc[:,'Erythrocytes'] = pd.Series(form.cleaned_data['Erythrocytes'])
        df.loc[:,'Leukocytes'] = pd.Series(form.cleaned_data['Leukocytes'])
        df.loc[:,'ALT'] = pd.Series(form.cleaned_data['ALT'])
        df.loc[:,'AST'] = pd.Series(form.cleaned_data['AST'])
        df.loc[:,'Albumen'] = pd.Series(form.cleaned_data['Albumen'])
        df.loc[:,'Basophils, %'] = pd.Series(form.cleaned_data['Basophils'])
        df.loc[:,'Eosinophils, %'] = pd.Series(form.cleaned_data['Eosinophils'])
        df.loc[:,'Lymphocytes, %'] = pd.Series(form.cleaned_data['Lymphocytes'])
        df.loc[:,'Monocytes, %'] = pd.Series(form.cleaned_data['Monocytes'])
        df.loc[:,'NEUT'] = pd.Series(form.cleaned_data['NEUT'])
        df.loc[:,'RDW'] = pd.Series(form.cleaned_data['RDW'])
        
        
        df.rename(columns={'Alpha-1-globulins1': 'Alpha-1-globulins'}, inplace=True)
        
        
        df.to_csv(settings.MEDIA_ROOT+"/../static/nnblood/patient_test.csv", index=False)
        
        
        try:
            command = "python django_call.py patient_test.csv" 
            pipe = subprocess.Popen(command.split(), 
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    cwd=settings.MEDIA_ROOT+"/../static/nnblood/")
            stdout_data, stderr_data = pipe.communicate()
            aaa = pipe.returncode
            if pipe.returncode != 0:
                raise RuntimeError("%r failed, status code %s stdout %r stderr %r" % (
                       command, pipe.returncode, stdout_data, stderr_data))
            result = stdout_data
        
            arResult = result.split('\n')
            age = arResult[1]
        except:
            raise
        
        #raise Exception('form')
        self.request.session['age'] = age
        return redirect(self.get_success_url())
    
        
    def form_invalid(self, form):
            return self.render_to_response(self.get_context_data(form=form))
        
        
class nnBloodResult(TemplateView):
    template_name = 'website/nn_blood_result.html'    
    
    
    
    def dispatch(self, request, *args, **kwargs):
        return super(nnBloodResult, self).dispatch(request, *args, **kwargs)
        
    
    def get_context_data(self, **kwargs):
        context = super(nnBloodResult, self).get_context_data(**kwargs)
        context['age'] = self.request.session['age']
        return context   
        
        
        
        
        
        
        
        
        
        
        
        
        
        