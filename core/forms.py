# -*- coding: utf-8 -*-

from django import forms

class CalculationParametersForm(forms.Form):
    sigma_num = forms.FloatField( label="Sigma ammount", initial=2)
    use_sigma = forms.BooleanField(label="Use sigma filter", initial=True)
    cnr_low = forms.FloatField(label="CNR lower limit", initial=0.67)
    cnr_up = forms.FloatField(label="CNR upper limit", initial=1.5)
    use_cnr = forms.BooleanField(label="Use CNR filter", initial=True)
    
    def __init__(self, *args, **kwargs):
        super(CalculationParametersForm, self).__init__(*args, **kwargs)
        self.fields['sigma_num'].widget.attrs.update({'class' : 'form-control'})
        self.fields['cnr_low'].widget.attrs.update({'class' : 'form-control'})
        self.fields['cnr_up'].widget.attrs.update({'class' : 'form-control'})
        
    
    