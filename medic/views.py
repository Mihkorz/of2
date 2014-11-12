import csv
from pandas import read_csv, read_excel, DataFrame

from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings

from .models import Nosology, TreatmentMethod
from profiles.models import Document


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
        num_responders = 0 # number of responders
        num_guessed_rigth = 0 # number of responders that remained status after voting
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
            
            ratio = float(Rcount)/float(len(path_cols))
            if ratio > 0.5 and status == 'RES':
                num_guessed_rigth+=1
            if ratio <= 0.5 and status == 'NRES':
                num_guessed_rigth+=1
                
                
            
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
        
        context['reliability'] = float(num_guessed_rigth)/float(all_samples)
        
        
        df_pms1 = read_excel(file_pms1, sheetname="PMS1")
        context['PMS1'] = df_pms1.to_html()
        
        return context
    
class PatientTreatmentDetail(DetailView):
    """ 
    Details for patient for each treatment
    """
    model = Document
    template_name = 'medic/patient_treatment_detail.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PatientTreatmentDetail, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(PatientTreatmentDetail, self).get_context_data(**kwargs)
        
        filename = settings.MEDIA_ROOT+"/"+self.object.document.name 
        
        treatment = TreatmentMethod.objects.get(pk=self.kwargs['treat_id'])
        
        file_pms1 = settings.MEDIA_ROOT+"/"+treatment.file_pms1.name
        file_probability = settings.MEDIA_ROOT+"/"+treatment.file_probability.name
        
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(open(file_probability, 'r').read(), delimiters='\t,;') # defining the separator of the csv file
        df_prob = read_csv(file_probability, delimiter=dialect.delimiter)
        df_output = read_excel(filename, sheetname="PMS1")        
        
        path_cols = [col for col in df_prob.columns if col not in ['Sample', 'group']]
        path_num = len(path_cols)
                
        df_pms1 = read_excel(file_pms1, sheetname="PMS1", index_col="Pathway").transpose()
        df_required_paths = df_pms1[path_cols]
        df_required_paths.reset_index(inplace="True")
        df_nres = df_required_paths[df_required_paths['index'].str.contains("NRES")]
        df_res = df_required_paths[~df_required_paths['index'].str.contains("NRES")]
        
        patient_responder = {}
        patient_nonresponder = {}
        
        for path_name in path_cols:
            from scipy.stats import norm 
            if path_name in df_output.index:
                patient_pms1 = df_output.loc[path_name.strip()].item()
            else:
                patient_pms1 = 0
                
            r_mean = df_res[path_name].mean(axis=1)
            r_std = df_res[path_name].std(axis=1)
            
            if patient_pms1 <= r_mean:
                    r_probability = norm.cdf(patient_pms1, r_mean, r_std)
            else:
                    r_probability = 1- norm.cdf(patient_pms1, r_mean, r_std)
                    
            patient_responder[path_name] = r_probability
            
            nr_mean = df_nres[path_name].mean(axis=1)
            nr_std = df_nres[path_name].std(axis=1)
            
            if patient_pms1 <= nr_mean:
                    nr_probability = norm.cdf(patient_pms1, nr_mean, nr_std)
            else:
                    nr_probability = 1- norm.cdf(patient_pms1, nr_mean, nr_std)
                    
            patient_nonresponder[path_name] = nr_probability
            
        dict_for_df={}
        dict_for_df['Responder'] = patient_responder
        dict_for_df['Nonresponder'] = patient_nonresponder
        
        df_patient = DataFrame.from_dict(dict_for_df).transpose()
        
        divided_df_patient = df_patient.T[df_patient.index[1]] / df_patient.T[df_patient.index[0]]
        patient_Rcount = 0
        for index, val in divided_df_patient.iteritems():
            if val>1:
                patient_Rcount+=1
        ratio = float(patient_Rcount)/float(path_num)
        
        lResponders = []
        lnonResponders = []
        flag_responder = 1
        patient_votes = float(patient_Rcount)/float(path_num)
        if ratio > 0.5:
            lResponders.append(patient_votes )
        else:
            lnonResponders.append(patient_votes)
            flag_responder = 0
            
        
            
            
                
        
                
        
        """ DRAW HISTOGRAM"""
        grouped = df_prob.groupby('Sample', sort=True)
        
        df_c = df_prob[df_prob['Sample'].str.contains("NRES")]
        all_samples = len(df_prob.index)/2
        num_nres_samples = len(df_c.index)/2 + len(lnonResponders)
        num_res_samples = (all_samples - num_nres_samples) +len(lResponders)
        
        num_responders = 0 # number of responders
        num_guessed_rigth = 0 # number of responders that remained status after voting
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
            ratio = float(Rcount)/float(len(path_cols))
            if status == 'RES':
                num_responders+=1
            if ratio > 0.5 and status == 'RES':
                num_guessed_rigth+=1
            if ratio <= 0.5 and status == 'NRES':
                num_guessed_rigth+=1
            
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
        context['flag_responder'] = flag_responder
        context['patient_votes'] = patient_votes
        context['reliability'] = float(num_guessed_rigth)/float(all_samples)
        
        
        
        context['treatment'] = treatment
        context['prob'] = df_prob.to_html()
        context['PMS1'] = df_pms1.to_html()
        return context
    
    
    
    
    
    
    
    
    
    