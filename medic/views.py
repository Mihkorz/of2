# -*- coding: utf-8 -*-
import csv
import json
import cairosvg

from pandas import read_csv, read_excel, DataFrame
from docx import Document as pyDocx
from docx.shared import Inches
from cStringIO import StringIO

from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
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
    Details page for particular treatment
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
                
        all_samples = len(df_prob.index)/2
                
        lResponders = []
        lnonResponders = []
        num_guessed_rigth = 0 # number of samples that remained status after voting
        num_guessed_wrong = 0 # number of samples that changed status after voting
        
        true_positive = 0
        true_negative = 0
        false_positive = 0
        false_negative = 0
        
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
                true_positive+=1
            if ratio > 0.5 and status == 'NRES':
                num_guessed_wrong+=1
                false_negative+=1
            if ratio <= 0.5 and status == 'NRES':
                num_guessed_rigth+=1
                true_negative+=1
            if ratio <= 0.5 and status == 'RES':
                num_guessed_wrong+=1
                false_positive+=1               
                
            
            len_p = len(path_cols)
            if status == 'NRES': 
                lnonResponders.append(float(Rcount)/float(len_p))
            else:
                lResponders.append(float(Rcount)/float(len_p) )
        from collections import Counter, OrderedDict
        
        nresponders = dict(Counter(lnonResponders))
        for x in nresponders:
            nresponders[x]/=float(all_samples)
            nresponders[x]*=100
        responders =  dict(Counter(lResponders))
        for x in responders:
            responders[x]/=float(all_samples)
            responders[x]*=100
        
        """ Statistical values """
        specificity = (float(true_negative))/(false_positive+true_negative)
        sensitivity = (float(true_positive))/(true_positive+false_negative)
        AUC = (specificity+sensitivity)/2
        accuracy = (true_positive+true_negative)/float(all_samples)
               
        context['nres'] = OrderedDict(sorted(nresponders.items()))
        context['res'] = OrderedDict(sorted(responders.items()))        
        context['prob'] = df_prob.to_html()        
        
        context['specificity'] = specificity
        context['sensitivity'] = sensitivity
        context['AUC'] = AUC
        context['accuracy'] = accuracy        
        
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
        num_guessed_wrong = 0 # number of samples that changed status after voting
        
        true_positive = 0
        true_negative = 0
        false_positive = 0
        false_negative = 0
        
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
                true_positive+=1
            if ratio > 0.5 and status == 'NRES':
                num_guessed_wrong+=1
                false_negative+=1
            if ratio <= 0.5 and status == 'NRES':
                num_guessed_rigth+=1
                true_negative+=1
            if ratio <= 0.5 and status == 'RES':
                num_guessed_wrong+=1
                false_positive+=1 
            
            len_p = len(path_cols)
            if status == 'NRES': 
                lnonResponders.append(float(Rcount)/float(len_p))
            else:
                lResponders.append(float(Rcount)/float(len_p) )
        from collections import Counter, OrderedDict
        
        nresponders = dict(Counter(lnonResponders))
        for x in nresponders:
            nresponders[x]/=float(all_samples)
            nresponders[x]*=100
        responders =  dict(Counter(lResponders))
        for x in responders:
            responders[x]/=float(all_samples)
            responders[x]*=100
               
        
        """ Statistical values """
        specificity = (float(true_negative))/(false_positive+true_negative)
        sensitivity = (float(true_positive))/(true_positive+false_negative)
        AUC = (specificity+sensitivity)/2
        accuracy = (true_positive+true_negative)/float(all_samples)
        
        context['nres'] = OrderedDict(sorted(nresponders.items()))
        context['res'] = OrderedDict(sorted(responders.items()))
        context['flag_responder'] = flag_responder
        context['patient_votes'] = patient_votes
        
        context['specificity'] = specificity
        context['sensitivity'] = sensitivity
        context['AUC'] = AUC
        context['accuracy'] = accuracy 
        
        
        treatment.treatment = treatment.treatment.replace('\n', ' ').replace('\r', '')
        
        
        context['treatment'] = treatment
        
        return context
    
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)
    
    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            lnres =  []
            for key, value in context['nres'].items():
                djson = {}
                djson.clear()
                djson['x']=key
                djson['y']=value
                if key == context['patient_votes'] and context['flag_responder']== 0:
                    djson['color']='red'
                lnres.append(djson)
            lres = []    
            for key, value in context['res'].items():
                djson = {}
                djson.clear()
                djson['x']=key
                djson['y']=value
                if key == context['patient_votes'] and context['flag_responder']== 1:
                    djson['color']='red'
                lres.append(djson)
                    
                    
            if context['flag_responder'] > 0:
                responder = 'responder'
            else:
                responder = 'non-responder'
                    
            data = {
                'nres': lnres,
                'res': lres,
                'treatment': context['treatment'].treatment,
                'patient_votes': round(context['patient_votes'], 2),
                'specificity': round(context['specificity'], 2),
                'sensitivity': round(context['sensitivity'], 2),
                'AUC': round(context['AUC'], 2),
                'accuracy': round(context['accuracy'], 2),
                'responder': responder,
                'num_of_patients': context['treatment'].num_of_patients,
                'histological_type': context['treatment'].histological_type,
                'grade': context['treatment'].grade,
                'hormone_receptor_status': context['treatment'].hormone_receptor_status,
                'her2_status': context['treatment'].her2_status,
                'stage': context['treatment'].stage,
                'citation': context['treatment'].citation,
                'organization_name': context['treatment'].organization_name,
                }
        
        return self.render_to_json_response(data)
    
class PatientTreatmentPDF(DetailView):
    """ 
    Details for all treatments as pdf
    """
    model = Document
    template_name = 'medic/patient_treatment_pdf.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PatientTreatmentPDF, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(PatientTreatmentPDF, self).get_context_data(**kwargs)
        
        hormone_status = self.object.parameters['hormone_status']
        her2_status = self.object.parameters['her2_status']
        
        treatments = TreatmentMethod.objects.filter(nosology=self.object.project.nosology)
        
        if hormone_status!='0':
                    treatments = treatments.filter(hormone_receptor_status=hormone_status)
                    
        if her2_status!='0':
                    treatments = treatments.filter(her2_status=her2_status)
        
        context['treatments'] = treatments
        
        return context    
    
    
class MedicAjaxGenerateReport(TemplateView):
    template_name = 'medic/patient_treatment_pdf.html'
    
    def post(self, request, *args, **kwargs):
        
        t_name = request.POST.get('t_name')
        t_n_patients = request.POST.get('t_n_patients')
        t_hist = request.POST.get('t_hist')
        t_grade = request.POST.get('t_grade')
        t_hormone = request.POST.get('t_hormone')
        t_her2 = request.POST.get('t_her2')
        t_stage = request.POST.get('t_stage')
        t_treatment = request.POST.get('t_treatment')
        t_cit = request.POST.get('t_cit')
        o_org = request.POST.get('o_org')
        svg = request.POST.get('svg')
        
        
        
        fout = open(settings.MEDIA_ROOT+'/output.png','w')
        
        cairosvg.svg2png(bytestring=svg,write_to=fout)

        fout.close()
        
        
        document = pyDocx()
        document.add_heading('Patient treatment report')
        
        document.add_page_break()
        document.add_heading('Treatment description:', level=2)
        
        document.add_paragraph(t_treatment)
        document.add_paragraph(t_n_patients)
        document.add_paragraph(t_hist)
        document.add_paragraph(t_grade)
        document.add_paragraph(t_hormone)
        document.add_paragraph(t_her2)
        document.add_paragraph(t_stage)
        document.add_paragraph(t_cit)
        document.add_paragraph(o_org)       
        document.add_picture(settings.MEDIA_ROOT+'/output.png', width=Inches(7.0))
        
        document.add_page_break()
        
        f = StringIO()
        document.save(f)
        
        response = HttpResponse(f.getvalue(), mimetype='application/vnd.ms-word')
        response['Content-Disposition'] = 'attachment; filename=PatientReport.docx'
        return response 
        


    
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        
        return super(MedicAjaxGenerateReport, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
              
        context = super(MedicAjaxGenerateReport, self).get_context_data(**kwargs)
        
        
        context['test'] = "TEst"
        
        return context
    
       
class MedicAjaxGenerateFullReport(TemplateView):
    template_name = 'medic/patient_treatment_pdf.html'
    
    def post(self, request, *args, **kwargs):
        
        
        document = pyDocx()
        document.add_heading('Patient treatment report')
        
        table = document.add_table(1, 2)
        table.allow_autofit = True
        table.style = 'TableGrid'
        # populate header row --------
        heading_cells = table.rows[0].cells
        heading_cells[0].text = 'Treatment'
        heading_cells[1].text = 'Patient status'
        
        
        
        
        for treat in TreatmentMethod.objects.filter(nosology = 1):
            treat_id = str(treat.id)
            cells = table.add_row().cells
            cells[0].text = request.POST.get('t_treatment'+treat_id)
            cells[1].text = request.POST.get('t_responder'+treat_id)
            
        document.add_page_break()
        
        for treat in TreatmentMethod.objects.filter(nosology = 1):
            
            treat_id = str(treat.id)
            
            t_n_patients = request.POST.get('t_n_patients'+treat_id)
            t_hist = request.POST.get('t_hist'+treat_id)
            t_grade = request.POST.get('t_grade'+treat_id)
            t_hormone = request.POST.get('t_hormone'+treat_id)
            t_her2 = request.POST.get('t_her2'+treat_id)
            t_stage = request.POST.get('t_stage'+treat_id)
            t_treatment = request.POST.get('t_treatment'+treat_id)
            t_cit = request.POST.get('t_cit'+treat_id)
            t_org = request.POST.get('t_org'+treat_id)
            svg = request.POST.get('svg'+treat_id)
            
            fout = open(settings.MEDIA_ROOT+'/medic/output.png','w')
        
            cairosvg.svg2png(bytestring=svg,write_to=fout)

            fout.close()
            
            document.add_heading('Treatment description:', level=2)
        
            document.add_paragraph('Treatment: '+t_treatment)
            document.add_paragraph('Number of patients: '+t_n_patients)
            document.add_paragraph('Histological type: '+t_hist)
            document.add_paragraph('Grade: ' + t_grade)
            document.add_paragraph('Hormone receptor status: '+t_hormone)
            document.add_paragraph('HER2 status: '+t_her2)
            document.add_paragraph('Stage: '+t_stage)
            document.add_paragraph('Citation(s): '+t_cit)
            document.add_paragraph('Organization name: '+t_org)       
            document.add_picture(settings.MEDIA_ROOT+'/medic/output.png', width=Inches(7.0))
        
            document.add_page_break()
            
        f = StringIO()
        document.save(f)
        
        response = HttpResponse(f.getvalue(), mimetype='application/vnd.ms-word')
        response['Content-Disposition'] = 'attachment; filename=PatientReport.docx'
        return response 
            
            
    
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        
        return super(MedicAjaxGenerateFullReport, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
              
        context = super(MedicAjaxGenerateFullReport, self).get_context_data(**kwargs)
        
        
        context['test'] = "TEst"
        
        return context    
    
    
    
    