# -*- coding: utf-8 -*-
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .forms import  CalculationParametersForm, MedicCalculationParametersForm
from profiles.models import Document



class OF3CalculationParameters(FormView):
    """
    Processes the form with calculation parameters, creates empty output Document, 
    creates Document in Process directory with PANDAS column 'Mean_Norm' and CNR for each gene     
    """
    
    template_name = 'core/of3_calculation_parameters.html'
    success_url = '/success/'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        input_document = Document.objects.get(pk=self.kwargs['pk'])
        
        if input_document.project.field == 'med':
            self.form_class = MedicCalculationParametersForm
        else:
            self.form_class = CalculationParametersForm       
        return super(OF3CalculationParameters, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(OF3CalculationParameters, self).get_context_data(**kwargs)
        
        input_document = Document.objects.get(pk=self.kwargs['pk'])
                
        context['document'] = input_document
        return context
    
    def form_valid(self, form):
                
        context = self.get_context_data()
        
        
        input_document = context['document']
        input_document_path = input_document.input_doc.document.name     
                
        """ 
        Assigning values from Calculation parameters form and controlling defaults.
        variable = form.cleaned_data.get('name of field in form', 'Default value if not found in form')  
        """
        #filters
        use_ttest = form.cleaned_data.get('use_ttest', True)
        use_fdr = form.cleaned_data.get('use_fdr', True)
        use_new_fdr = form.cleaned_data.get('use_new_fdr', True)
        use_ttest_1sam = form.cleaned_data.get('use_ttest_1sam', False) 
        pvalue_threshold = form.cleaned_data.get('pvalue_threshold', 0.05)
        qvalue_threshold = form.cleaned_data.get('qvalue_threshold', 0.05)        
        use_percent_single = form.cleaned_data.get('use_percent_single', False)
        use_percent_all = form.cleaned_data.get('use_percent_all', False)
        percent_threshold = form.cleaned_data.get('percent_threshold', 5)
        use_cnr = form.cleaned_data.get('use_cnr', True)
        cnr_low = form.cleaned_data.get('cnr_low', 0.67)
        cnr_up =  form.cleaned_data.get('cnr_up', 1.5)
        use_sigma = form.cleaned_data.get('use_sigma', False) # !!! deprecated !!! 
        sigma_num = form.cleaned_data.get('sigma_num', 2) # !!! deprecated !!!
        
        #database and normal choice
        organism_choice = form.cleaned_data.get('organism_choice', 'human') #default=human
        db_choice = form.cleaned_data.get('db_choice', ['primary_old']) #default=primary_old
        db_choice_drug = form.cleaned_data.get('db_choice_drug', ['oncofinder']) #default=oncofinder
        norm_choice = form.cleaned_data.get('norm_choice', 2) #default=geometric 
        
        #what to calculate and include in output report
        calculate_pas = form.cleaned_data.get('calculate_pas', False)
        calculate_pas1 = form.cleaned_data.get('calculate_pas1', True)
        calculate_pas2 = form.cleaned_data.get('calculate_pas2', False)
        calculate_ds1a = form.cleaned_data.get('calculate_ds1a', False)
        calculate_ds2 = form.cleaned_data.get('calculate_ds2', False)
        calculate_ds1b = form.cleaned_data.get('calculate_ds1b', False)
        calculate_norms_pas = form.cleaned_data.get('calculate_norms_pas', False)
        calculate_pvalue_each = form.cleaned_data.get('calculate_pvalue_each', False)
        calculate_pvalue_all = form.cleaned_data.get('calculate_pvalue_all', False)
        calculate_FDR_each = form.cleaned_data.get('calculate_FDR_each', False)
        calculate_FDR_all = form.cleaned_data.get('calculate_FDR_all', False)  
        new_pathway_names = form.cleaned_data.get('new_pathway_names', False)
        diff_genes_amount = form.cleaned_data.get('diff_genes_amount', False)
        
        
        filters = {               'sigma_num': sigma_num,
                                 'use_sigma': use_sigma,
                                 'cnr_low': cnr_low,
                                 'cnr_up': cnr_up,
                                 'use_cnr': use_cnr,
                                 'use_ttest': use_ttest,
                                 'use_fdr': use_fdr,
                                 'use_new_fdr': use_new_fdr,
                                 'use_ttest_1sam': use_ttest_1sam,
                                 'use_percent_single': use_percent_single,
                                 'use_percent_all': use_percent_all,
                                 'norm_algirothm': 'geometric' if int(norm_choice)>1 else 'arithmetic',
                                 'organism': organism_choice, 
                                 'db': db_choice,
                                 'db_choice_drug': db_choice_drug,
                                 'pvalue_threshold': pvalue_threshold,
                                 'qvalue_threshold': qvalue_threshold,
                                 'percent_threshold': percent_threshold
                                 
                                 }
        output_values = {
                         'calculate_pas': calculate_pas,
                         'calculate_pas1': calculate_pas1,
                         'calculate_pas2': calculate_pas2,
                         'calculate_ds1a': calculate_ds1a,
                         'calculate_ds1b': calculate_ds1b,
                         'calculate_ds2': calculate_ds2,
                         'calculate_norms_pas': calculate_norms_pas,
                         'calculate_pvalue_each': calculate_pvalue_each,
                         'calculate_pvalue_all':calculate_pvalue_all,
                         'calculate_FDR_each': calculate_FDR_each,
                         'calculate_FDR_all': calculate_FDR_all,
                         'new_pathway_names': new_pathway_names,
                         'diff_genes_amount': diff_genes_amount
                         
                         
                         }
        
        
        raise Exception('OF3 FORM')
        return True
    
    def form_invalid(self, form):
            return self.render_to_response(self.get_context_data(form=form))
        
        
        
            