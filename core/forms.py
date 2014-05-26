# -*- coding: utf-8 -*-

from django import forms

class CalculationParametersForm(forms.Form):
    sigma_num = forms.FloatField( label="Sigma ammount", initial=2, required=False)
    use_sigma = forms.BooleanField(label="Use sigma filter", initial=True, required=False)
    cnr_low = forms.FloatField(label="CNR lower limit", initial=0.67, required=False)
    cnr_up = forms.FloatField(label="CNR upper limit", initial=1.5, required=False)
    use_cnr = forms.BooleanField(label="Use CNR filter", initial=True, required=False)
    
    def __init__(self, *args, **kwargs):
        super(CalculationParametersForm, self).__init__(*args, **kwargs)
        self.fields['sigma_num'].widget.attrs.update({'class' : 'form-control'})
        self.fields['cnr_low'].widget.attrs.update({'class' : 'form-control'})
        self.fields['cnr_up'].widget.attrs.update({'class' : 'form-control'})
        
    
    