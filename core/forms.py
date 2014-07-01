# -*- coding: utf-8 -*-

from django import forms

class CalculationParametersForm(forms.Form):
    
    NORM_CHOICES = (('1', 'arithmetic',),
                    ('2', 'geometric',))
    
    sigma_num = forms.FloatField( label="Sigma amount", initial=2, required=False)
    use_sigma = forms.BooleanField(label="Use sigma filter", initial=True, required=False)
    cnr_low = forms.FloatField(label="CNR lower limit", initial=0.67, required=False)
    cnr_up = forms.FloatField(label="CNR upper limit", initial=1.5, required=False)
    use_cnr = forms.BooleanField(label="Use CNR filter", initial=True, required=False)
    norm_choice = forms.ChoiceField(label="Choose calculation algorithm for normal values",
                                     widget=forms.RadioSelect, choices=NORM_CHOICES, initial=1)
    
    def __init__(self, *args, **kwargs):
        super(CalculationParametersForm, self).__init__(*args, **kwargs)
        self.fields['sigma_num'].widget.attrs.update({'class' : 'form-control'})
        self.fields['cnr_low'].widget.attrs.update({'class' : 'form-control'})
        self.fields['cnr_up'].widget.attrs.update({'class' : 'form-control'})
       
        
    
    