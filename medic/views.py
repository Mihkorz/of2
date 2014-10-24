import csv
from pandas import read_csv, read_excel, DataFrame

from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings

from .models import Nosology, TreatmentMethod


class MedicNosologyList(ListView):
    """
    List of Nosologies for Medic DB section
    """    
    model = Nosology
    template_name = 'medic/medic_nosology_list.html'
    context_object_name = 'nosologies'
    paginate_by = 20
        
    def get_context_data(self, **kwargs):
        context = super(MedicNosologyList, self).get_context_data(**kwargs)        
        return context
        
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MedicNosologyList, self).dispatch(request, *args, **kwargs)
    
class MedicNosologyDetail(DetailView):
    """
    Details page for particular nosology
    """
    model = Nosology
    template_name = 'medic/medic_nosology_detail.html'
    context_object_name = 'nosology'    
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MedicNosologyDetail, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(MedicNosologyDetail, self).get_context_data(**kwargs)
        
        return context
    
class MedicTreatmentDetail(DetailView):
    """
    Details page for particular nosology
    """
    model = TreatmentMethod
    template_name = 'medic/medic_treatment_detail.html'
    context_object_name = 'treatment'    
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MedicTreatmentDetail, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(MedicTreatmentDetail, self).get_context_data(**kwargs)
        
        file_pms1 = settings.MEDIA_ROOT+"/"+self.object.file_pms1.name
        file_probability = settings.MEDIA_ROOT+"/"+self.object.file_probability.name
        
        
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(open(file_probability, 'r').read(), delimiters='\t,;') # defining the separator of the csv file
        df_prob = read_csv(file_probability, delimiter=dialect.delimiter)
        grouped = df_prob.groupby('Sample')
        
        dictcount = {}
        for name, group in grouped:
            status = name.split('_')[1]
            path_cols = [col for col in group.columns if col not in ['Sample']]
            path_df = group[path_cols]
            
            raise
        
        context['prob'] = grouped.groups
        
        cols = [col for col in df_prob.columns if col not in ['Sample', 'group']]
        df_pathways = df_prob[cols]
        
        context['ncol'] = len(cols)
        context['test'] = df_pathways[:50].to_html()
        
        df_pms1 = read_excel(file_pms1, sheetname="PMS1")
        context['PMS1'] = df_pms1[:50].to_html()
        
        return context
    
