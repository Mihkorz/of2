# -*- coding: utf-8 -*-

from pandas import DataFrame, read_csv
from rpy2.robjects.packages import importr
import pandas.rpy.common as com
import csv
import numpy as np

from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .forms import XpnParametersForm


class XpnForm(FormView):
    
    form_class = XpnParametersForm
    success_url = '/thanks/'
    
    template_name = 'core/xpnform.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(XpnForm, self).dispatch(request, *args, **kwargs)
        
    
    def get_context_data(self, **kwargs):        
        context = super(XpnForm, self).get_context_data(**kwargs)
        
        context['test'] = 'test'
        return context
    
    def form_valid(self, form):
        
        pl1 = form.cleaned_data.get('pl1', False)
        pl2 = form.cleaned_data.get('pl2', False)
        k = form.cleaned_data.get('k', 10)
        l = form.cleaned_data.get('l', 4)
        log_scale = form.cleaned_data.get('log_scale', True)
        p1_names = form.cleaned_data.get('p1_names', 1)
        p2_names = form.cleaned_data.get('p2_names', 1)
        gene_cluster = form.cleaned_data.get('gene_cluster', 'kmeans')
        assay_cluster = form.cleaned_data.get('assay_cluster', 'kmeans')
        corr = form.cleaned_data.get('corr', 'pearson')
        iterations = form.cleaned_data.get('iterations', 30)
        skip_match = form.cleaned_data.get('skip_match', False) 
        
        sniffer = csv.Sniffer()
        dialect_pl1 = sniffer.sniff(pl1.read(), delimiters='\t,;') # defining the separator of the csv file
        pl1.seek(0)
        df_pl1 = read_csv(pl1, delimiter=dialect_pl1.delimiter)
                
        dialect_pl2 = sniffer.sniff(pl2.read(), delimiters='\t,;') # defining the separator of the csv file
        pl2.seek(0)
        df_pl2 = read_csv(pl2, delimiter=dialect_pl2.delimiter)
        
        if log_scale:
            def apply_log(col):
                try:
                    np.log(col)
                except:
                    pass
                return col
            df_pl1 = df_pl1.apply(apply_log, axis=0).fillna(0)
            df_pl2 = df_pl2.apply(apply_log, axis=0).fillna(0)
        
        
        Rdf_pl1 = com.convert_to_r_dataframe(df_pl1)
        Rdf_pl2 = com.convert_to_r_dataframe(df_pl2)
        try:
            conor = importr("CONOR")
            R_output = conor.xpn(Rdf_pl1, Rdf_pl2, p1_names=p1_names, p2_names=p2_names,
                                 iterations=iterations, K=k, L=l )
        except:
            raise
        py_output = com.convert_robj(R_output)

        df_out_x = DataFrame(py_output['x'])
        df_out_y = DataFrame(py_output['y'])        
        df_out_x.index.name = df_out_y.index.name = 'SYMBOL'
        
        df_output_all = df_out_x.join(df_out_y, lsuffix='_x', rsuffix='_y')
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="'+pl1.name+pl2.name+'.csv"'
        
        df_output_all.to_csv(response)
        
        return response
        
    
    def form_invalid(self, form):
            return self.render_to_response(self.get_context_data(form=form)) 