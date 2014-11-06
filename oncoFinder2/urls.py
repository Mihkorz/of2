# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic.base import  RedirectView

from django.contrib import admin
admin.autodiscover()

from website.views import IndexPage, AboutPage, Logout
from profiles.views import ProfileIndex, SettingsProfile, SettingsBilling, CreateProject, \
                           DeleteProject, ProjectDetail, CreateDocument, DeleteDocument, \
                           DocumentDetail, SampleDetail, AjaxPathDetail
                           
from core.views import CoreSetCalculationParameters, CoreCalculation, Test, Celery, TaskStatus
from database.views import PathwayList, PathwayDetail, PathwayAjaxSearch, \
                           DrugList, DrugDetail, DrugAjaxSearch
from metabolism.views import MetabolismPathwayList, MetabolismPathwayDetail, \
                             MetabolismPathwayAjaxSearch
from mouse.views import MousePathwayList, MousePathwayDetail, \
                             MousePathwayAjaxSearch, MouseTest, MouseMapping
from medic.views import MedicNosologyList, MedicNosologyDetail, MedicTreatmentDetail, \
                        PatientTreatmentDetail

urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT}),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),
    url(r'^admin/', include(admin.site.urls)),
                       
    ################### Website App ##############################                
    url(r'^$', IndexPage.as_view(), name="website_index"),
    url(r'^ws/about/$', AboutPage.as_view(), name="website_about"),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'website/login.html'}),
    url(r'^logout$', Logout.as_view(), name="logout"),
    
    
    ################### Profiles App ##############################
    url(r'^user/(?P<slug>[-\w]+)/$', ProfileIndex.as_view(), name="profiles_index"),
    url(r'^settings/profile/$', SettingsProfile.as_view(), name="settings_profile"),
    url(r'^settings/billing/$', SettingsBilling.as_view(), name="settings_billing"),
    
    url(r'^project/new/$', CreateProject.as_view(), name="project_create"),
    url(r'^project/delete/(?P<pk>\d+)/$', DeleteProject.as_view(), name="project_delete"),
    url(r'^project/(?P<slug>[-\w]+)/$', ProjectDetail.as_view(), name="project_detail"),
    
    url(r'^document/new/$', CreateDocument.as_view(), name="document_create"),
    url(r'^document/delete/(?P<pk>\d+)/$', DeleteDocument.as_view(), name="document_delete"),
    url(r'^document/doc(?P<pk>\d+)/$', DocumentDetail.as_view(), name="document_detail"),
    url(r'^document/doc(?P<pk>\d+)/treat(?P<treat_id>.*)/$', PatientTreatmentDetail.as_view(), name="patient_treatment_detail"),
    url(r'^document/doc(?P<pk>\d+)/(?P<sample_name>.*)/$', SampleDetail.as_view(), name="sample_detail"),
    
    
    url(r'^document/ajaxpathdetail/$', AjaxPathDetail.as_view(), name="ajax_path_detail"),
    
    ################### Core App ##############################
    url(r'^calculation-parameters/doc(?P<pk>\d+)/$', CoreSetCalculationParameters.as_view(), name="core_set_calculation_parameters"),
    url(r'^calculation/doc(?P<pk>\d+)/$', CoreCalculation.as_view(), name="core_calculation"),
    
    url(r'^test/$', Test.as_view()),
    url(r'^celery/$', Celery.as_view()),
    url(r'^task_status/$', TaskStatus.as_view()),
    
    ################### DataBase App ##############################
    url(r'^db/pathways/$', PathwayList.as_view(), name="pathway_list"),
    url(r'^db/pathways/[-\w]+/(?P<pk>\d+)/$', PathwayDetail.as_view(), name="pathway_detail"),
    url(r'^db/pathways/search/$', PathwayAjaxSearch.as_view(), name="pathway_ajax_search"),
    url(r'^db/drugs/$', DrugList.as_view(), name="drug_list"),
    url(r'^db/drugs/[-\w]+/(?P<pk>\d+)/$', DrugDetail.as_view(), name="drug_detail"),
    url(r'^db/drugs/search/$', DrugAjaxSearch.as_view(), name="drug_ajax_search"),
    
    ################### Metabolism App ##############################
    url(r'^metabolism/pathways/$', MetabolismPathwayList.as_view(), name="metabolism_pathway_list"),
    url(r'^metabolism/pathways/[-\w]+/(?P<pk>\d+)/$', MetabolismPathwayDetail.as_view(), name="metabolism_pathway_detail"),
    url(r'^metabolism/pathways/search/$', MetabolismPathwayAjaxSearch.as_view(), name="metabolism_pathway_ajax_search"),
    
    ################### Mouse App ##############################
    url(r'^mouse/pathways/$', MousePathwayList.as_view(), name="mouse_pathway_list"),
    url(r'^mouse/pathways/[-\w]+/(?P<pk>\d+)/$', MousePathwayDetail.as_view(), name="mouse_pathway_detail"),
    url(r'^mouse/pathways/search/$', MousePathwayAjaxSearch.as_view(), name="mouse_pathway_ajax_search"),
    url(r'^mouse/mapping/$', MouseMapping.as_view(), name="mouse_mapping"),
    url(r'^mouse/test/$', MouseTest.as_view(), name="mouse_test"), 

    ################### Medic App ##############################
    url(r'^db/medic/$', MedicNosologyList.as_view(), name="medic_nosology_list"),
    url(r'^db/medic/[-\w]+/(?P<pk>\d+)/$', MedicNosologyDetail.as_view(), name="medic_nosology_detail"),
    url(r'^db/medic/[-\w]+/[-\w]+/[-\w]+/(?P<pk>\d+)/$', MedicTreatmentDetail.as_view(), name="medic_treatment_detail"),
    #url(r'^mouse/pathways/[-\w]+/(?P<pk>\d+)/$', MousePathwayDetail.as_view(), name="mouse_pathway_detail"),


    
    

   
)
