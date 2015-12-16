# -*- coding: utf-8 -*-

from django import forms
from profiles.models import ShambalaDocument

class CalculationParametersForm(forms.Form):
    
    NORM_CHOICES = (('2', 'Geometric',),
                    ('1', 'Arithmetic',))
    
    ORGANISM_CHOICES = (('human', 'Human',),
                       ('mouse', 'Mouse',))
    
    DB_CHOICES = (('primary_old', 'Primary Pathway Database (old)'),
                  ('primary_new', 'Primary Pathway Database (new)'),
                  ('metabolism', 'Metabolism Pathway Database'),
                  ('cytoskeleton', 'Cytoskeleton Pathway Database'),
                  ('kegg', 'KEGG Pathway Database'),
                  ('nci', 'NCI Pathway Database'),
                  ('biocarta', 'Biocarta'),
                  ('kegg_adjusted', 'KEGG Adjusted Pathway Database'),
                  ('kegg_10', 'KEGG >10 genes'),
                  ('kegg_adjusted_10', 'KEGG Adjusted >10 genes'),)
    DB_CHOICES_DRUG = (('oncofinder', 'OncoFinder'),
                       ('geroscope', 'GeroScope'),
                      )
    #FILTERS
    use_sigma = forms.BooleanField(label="Use sigma filter", initial=False, required=False)
    sigma_num = forms.FloatField( label="Sigma amount \n (deprecated)", initial=2, required=False)
    use_cnr = forms.BooleanField(label="Use CNR filter", initial=True, required=False)
    cnr_low = forms.FloatField(label="CNR lower limit", initial=0.67, required=False)
    cnr_up = forms.FloatField(label="CNR upper limit", initial=1.5, required=False)
    use_ttest = forms.BooleanField(label="Use T-test for gene distribution ",
                                   initial=True, required=False)
    use_fdr = forms.BooleanField(label="Use Benjamini FDR for T-test ",
                                   initial=True, required=False)
    use_new_fdr = forms.BooleanField(label="New  Storey FDR for T-test ",
                                   initial=False, required=False)
    use_ttest_1sam = forms.BooleanField(label="Use 1sample T-test ",
                                   initial=False, required=False)
    pvalue_threshold = forms.FloatField( label="p-value threshold", initial=0.05, required=False)
    qvalue_threshold = forms.FloatField( label="q-value threshold", initial=0.05, required=False)
    
    #For OF_cnr_stat files only!
    use_ttest_stat = forms.BooleanField(label="Use p-values",
                                   initial=True, required=False)
    use_fdr_stat = forms.BooleanField(label="Use q-values",
                                   initial=False, required=False)
    
    #organism DB and norm algorithm selection
    organism_choice = forms.ChoiceField(label="Organism",
                                     widget=forms.RadioSelect, choices=ORGANISM_CHOICES, initial='human')
    db_choice = forms.MultipleChoiceField(label="Pathway DataBase",
                                     widget=forms.SelectMultiple, choices=DB_CHOICES, initial=['primary_old'])
    db_choice_drug = forms.MultipleChoiceField(label="Drug DataBase",
                                     widget=forms.SelectMultiple, choices=DB_CHOICES_DRUG, initial=['oncofinder'])
    norm_choice = forms.ChoiceField(label="Calculation algorithm for normal values",
                                     widget=forms.RadioSelect, choices=NORM_CHOICES, initial=2)
    #values included into report
    calculate_pas = forms.BooleanField(label="PAS", initial=True, required=False)
    calculate_pas1 = forms.BooleanField(label="PAS1", initial=True, required=False)
    calculate_pas2 = forms.BooleanField(label="PAS2", initial=True, required=False)
    calculate_ds1a = forms.BooleanField(label="DS1A", initial=False, required=False)
    calculate_ds1b = forms.BooleanField(label="DS1B", initial=False, required=False)
    calculate_ds2 = forms.BooleanField(label="DS2", initial=False, required=False)    
    calculate_norms_pas = forms.BooleanField(label="PAS1 for Norms(requires at least 3 norms)", initial=True, required=False)
    calculate_pvalue_each = forms.BooleanField(label="P-value for each sample(parametric test)", initial=True, required=False)
    calculate_pvalue_all = forms.BooleanField(label="P-value for each pathway(non-parametric test)", initial=True, required=False)
    calculate_FDR_each = forms.BooleanField(label="q-value for each sample(parametric test)", initial=False, required=False)
    calculate_FDR_all = forms.BooleanField(label="q-value for each pathway(non-parametric test)", initial=False, required=False)
    
    new_pathway_names = forms.BooleanField(label="New pathway names", initial=False, required=False)
    
    diff_genes_amount = forms.BooleanField(label="Differential genes amount and ratio ", initial=False, required=False)
    
    
    
    def __init__(self, *args, **kwargs):
        super(CalculationParametersForm, self).__init__(*args, **kwargs)
        self.fields['sigma_num'].widget.attrs.update({'class' : 'form-control input-sm'})
        self.fields['pvalue_threshold'].widget.attrs.update({'class' : 'form-control input-sm', 'style':'width:60px; display:inline'})
        self.fields['qvalue_threshold'].widget.attrs.update({'class' : 'form-control input-sm', 'style':'width:60px; display:inline'})
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
        
class HarmonyParametersForm(forms.Form):
    pl1 = forms.FileField(label="Platform1 data", required=False)
    pl2 = forms.FileField(label="Platform2 data", required=False)
    log_scale = forms.BooleanField(label="log_scale", initial=True, required=False)
    k = forms.IntegerField(label="K", initial=10, required=False)
    l = forms.IntegerField(label="L", initial=4, required=False)
    p1_names = forms.IntegerField(label="p1.names", initial=0, required=False)
    p2_names = forms.IntegerField(label="p2.names", initial=0, required=False)
    gene_cluster = forms.CharField(label="gene.cluster", initial="kmeans", required=False)
    assay_cluster = forms.CharField(label="assay.cluster", initial="kmeans", required=False)
    corr = forms.CharField(label="corr", initial="pearson", required=False)
    iterations = forms.IntegerField(label="iterations", initial=30, required=False)
    skip_match = forms.BooleanField(label="skip.match", initial=False, required=False)
    
    def __init__(self, *args, **kwargs):
        super(HarmonyParametersForm, self).__init__(*args, **kwargs)
        self.fields['pl1'].widget.attrs.update({'class' : 'form-control input-sm', 'style':'width:200px; display:inline'})
        self.fields['pl2'].widget.attrs.update({'class' : 'form-control input-sm', 'style':'width:200px; display:inline'})
        
        self.fields['k'].widget.attrs.update({'class' : 'form-control input-sm', 'style':'width:50px; display:inline'})
        self.fields['l'].widget.attrs.update({'class' : 'form-control input-sm', 'style':'width:50px; display:inline'})
        self.fields['p1_names'].widget.attrs.update({'class' : 'form-control input-sm', 'style':'width:50px; display:inline'})
        self.fields['p2_names'].widget.attrs.update({'class' : 'form-control input-sm', 'style':'width:50px; display:inline'})
        self.fields['iterations'].widget.attrs.update({'class' : 'form-control input-sm', 'style':'width:50px; display:inline'})
        
        self.fields['gene_cluster'].widget.attrs.update({'class' : 'form-control input-sm'})
        self.fields['assay_cluster'].widget.attrs.update({'class' : 'form-control input-sm'})
        self.fields['corr'].widget.attrs.update({'class' : 'form-control input-sm'})


class ShambalaParametersForm(forms.ModelForm):
    class Meta(object):
        model = ShambalaDocument
        fields = ['document', 'auxiliary', 'log_scale' ]
                    
    
    
    def __init__(self, *args, **kwargs):
        super(ShambalaParametersForm, self).__init__(*args, **kwargs)
        
        self.fields['document'].widget.attrs.update({'class' : 'form-control input-sm', 
                                                'style':'width:200px; display:inline'})
        







    