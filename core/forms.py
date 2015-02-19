# -*- coding: utf-8 -*-

from django import forms

class CalculationParametersForm(forms.Form):
    
    NORM_CHOICES = (('2', 'Geometric',),
                    ('1', 'Arithmetic',))
    
    DB_CHOICES = (('1', 'Human',),
                  ('3', 'Mouse'),
                  ('2', 'Metabolism',))
    #FILTERS
    use_sigma = forms.BooleanField(label="Use sigma filter", initial=False, required=False)
    sigma_num = forms.FloatField( label="Sigma amount \n (deprecated)", initial=2, required=False)
    use_cnr = forms.BooleanField(label="Use CNR filter", initial=True, required=False)
    cnr_low = forms.FloatField(label="CNR lower limit", initial=0.67, required=False)
    cnr_up = forms.FloatField(label="CNR upper limit", initial=1.5, required=False)
    use_ttest = forms.BooleanField(label="Use two-sided T-test ",
                                   initial=True, required=False)
    pvalue_num = forms.FloatField( label="P-value threshold", initial=0.05, required=False)
    #DB and norm algorithm selection
    db_choice = forms.ChoiceField(label="Pathway DataBase",
                                     widget=forms.RadioSelect, choices=DB_CHOICES, initial=1)
    norm_choice = forms.ChoiceField(label="Calculation algorithm for normal values",
                                     widget=forms.RadioSelect, choices=NORM_CHOICES, initial=2)
    #values included into report
    calculate_pas = forms.BooleanField(label="PAS", initial=True, required=False)
    calculate_pas1 = forms.BooleanField(label="PAS1", initial=True, required=False)
    calculate_pas2 = forms.BooleanField(label="PAS2", initial=True, required=False)
    calculate_ds1 = forms.BooleanField(label="DS1A", initial=False, required=False)
    calculate_ds2 = forms.BooleanField(label="DS2", initial=False, required=False)
    calculate_ds3 = forms.BooleanField(label="DS1B", initial=False, required=False)
    calculate_norms_pas = forms.BooleanField(label="PAS1 for Norms(requires at least 3 norms)", initial=True, required=False)
    calculate_pvalue_each = forms.BooleanField(label="P-value for each sample(parametric test)", initial=True, required=False)
    calculate_pvalue_all = forms.BooleanField(label="P-value for each pathway(non-parametric test)", initial=True, required=False)
    
    new_pathway_names = forms.BooleanField(label="New pathway names", initial=False, required=False)
    
    
    def __init__(self, *args, **kwargs):
        super(CalculationParametersForm, self).__init__(*args, **kwargs)
        self.fields['sigma_num'].widget.attrs.update({'class' : 'form-control input-sm'})
        self.fields['pvalue_num'].widget.attrs.update({'class' : 'form-control input-sm'})
        self.fields['cnr_low'].widget.attrs.update({'class' : 'form-control input-sm'})
        self.fields['cnr_up'].widget.attrs.update({'class' : 'form-control input-sm'})
       
        
class MedicCalculationParametersForm(forms.Form):
    
    HORMONE_STASUS_CHOICES = (('0', 'Unspecified'),
                    ('ER positive', 'ER positive',),
                    ('ER negative', 'ER negative',))
    
    hormone_status = forms.ChoiceField(label="Hormone receptor status",
                                     choices=HORMONE_STASUS_CHOICES, initial=0)
    
    HER2_STASUS_CHOICES = (('0', 'Unspecified'),
                    ('positive', 'positive',),
                    ('negative', 'negative',))
    
    her2_status = forms.ChoiceField(label="HER2 status",
                                     choices=HER2_STASUS_CHOICES, initial=0)
        
    