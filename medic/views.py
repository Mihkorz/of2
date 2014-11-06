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
        grouped = df_prob.groupby('Sample', sort=True)
        
        df_c = df_prob[df_prob['Sample'].str.contains("NRES")]
        all_samples = len(df_prob.index)/2
        num_nres_samples = len(df_c.index)/2
        num_res_samples = (all_samples - num_nres_samples)
        
        lResponders = []
        lnonResponders = []
        for name, group in grouped:
            status = name.split('_')[1].strip()
            path_cols = [col for col in group.columns if col not in ['Sample', 'group']]
            path_df = group[path_cols]
            #raise
            divided_df = path_df.T[path_df.index[1]] / path_df.T[path_df.index[0]]
            Rcount = 0 # count Responder votes
            for index, val in divided_df.iteritems():
                if val>1:
                    Rcount+= 1
            
            len_p = len(path_cols)
            if status == 'NRES': 
                lnonResponders.append(float(Rcount)/float(len_p))
            else:
                lResponders.append(float(Rcount)/float(len_p) )
        from collections import Counter, OrderedDict
        
        nresponders = dict(Counter(lnonResponders))
        for x in nresponders:
            nresponders[x]/=float(num_nres_samples)
            nresponders[x]*=100
        responders =  dict(Counter(lResponders))
        for x in responders:
            responders[x]/=float(num_res_samples)
            responders[x]*=100
               
        context['nres'] = OrderedDict(sorted(nresponders.items()))
        context['res'] = OrderedDict(sorted(responders.items()))
        
        context['prob'] = df_prob.to_html()
        
        cols = [col for col in df_prob.columns if col not in ['Sample', 'group']]
        df_pathways = df_prob[cols]
        
        context['ncol'] = len(cols)
        context['test'] = df_pathways[:50].to_html()
        
        df_pms1 = read_excel(file_pms1, sheetname="PMS1")
        context['PMS1'] = df_pms1[:50].to_html()
        
        return context
    
