# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic.base import  RedirectView

from django.contrib import admin
admin.autodiscover()

from website.views import IndexPage, AboutPage, Logout

from website.loreal_report_views import LorealReport, \
                                 LorealReportGeneTableJson, LorealReportGeneScatterJson, LorealReportGeneDetailJson, LorealReportGeneBoxplotJson, \
                                 LorealReportPathwayScatterJson, LorealReportPathwayTableJson, LorealReportAjaxPathDetail, \
                                 LorealReportAjaxPathwayVenn, LorealReportAjaxPathwayVennTable
from website.pathdemo_report_views import PathDemoReport
from website.demo2_report_views import Demo2Report, Demo2GeneVolcanoJson, Demo2ReportGeneTableJson, Demo2ReportGeneBoxplotJson,\
                                    Demo2ReportPathwayTableJson, Demo2ReportAjaxPathDetail, \
                                    Demo2ReportAjaxPathwayVenn, Demo2ReportAjaxPathwayVennTable                                
from website.lrl_report_views import LRLReport,\
                                     LRLReportGeneScatterJson, LRLReportGeneTableJson, LRLReportGeneDetailJson, \
                                     LRLGeneVolcanoJson, LRLReportPathwayTableJson, LRLReportSideEffTableJson, \
                                     LRLReportAjaxPathDetail, LRLReportAjaxPathLine, LRLReportGeneBoxplotJson

from website.bt_report_views import BTReport, \
                                    BTGeneVolcanoJson, BTReportGeneTableJson, BTReportGeneBoxplotJson,\
                                    BTReportPathwayTableJson, BTReportAjaxPathDetail, \
                                    BTReportAjaxPathwayVenn, BTReportAjaxPathwayVennTable
from website.gp_report_views import GPReport, \
                                    GPReportPathwayTableJson, GPReportAjaxPathwayVenn, GPReportAjaxPathwayVennTable, \
                                    GPReportAjaxPathDetail
from website.demo_report_views import DemoReport, ReportJson                         

from website.nn_views import nnBloodView, nnBloodResult 

from profiles.views import ProfileIndex, SettingsProfile, SettingsBilling, CreateProject, \
                           DeleteProject, ProjectDetail, CreateDocument, DeleteDocument, \
                           DocumentDetail, SampleDetail, AjaxPathDetail
                           
from core.views import CoreSetCalculationParameters, CoreCalculation, Test
from core.of3_views import OF3CalculationParameters 
from core.harmony_views import ShambalaForm, ShambalaDone, \
                               HarmonyForm, HarmonyDone, HarmonyPrevFiles, \
                               breastmodule
from core.utils_views import ConvertPath
from database.views import PathwayList, PathwayDetail, PathwayAjaxSearch, \
                           DrugList, DrugDetail, DrugAjaxSearch
from metabolism.views import MetabolismPathwayList, MetabolismPathwayDetail, \
                             MetabolismPathwayAjaxSearch
from mouse.views import MousePathwayList, MousePathwayDetail, MousePathwayAjaxSearch, \
                        MouseTest, MouseMapping, MouseMetabolismPathwayList, \
                        MouseMetabolismPathwayDetail, MouseMetabolismPathwayAjaxSearch
from medic.views import MedicNosologyList, MedicNosologyDetail, MedicTreatmentDetail, \
                        PatientTreatmentDetail, PatientTreatmentPDF, MedicAjaxGenerateReport, \
                        MedicAjaxGenerateFullReport, MedicPatientCalculation, MedicTest
from mirna.views import MirnaSetCalculationParameters

from core.celery_views import Celery, TaskStatus

from report.views import ReportList, ReportDetail, \
                         ReportGeneVolcanoJson, ReportGeneScatterJson, ReportGeneTableJson, ReportGeneTableScatterJson,\
                         ReportGeneBoxplotJson, ReportGeneBarplotJson, \
                         ReportAjaxPathwayVenn, ReportAjaxPathwayVennTable, ReportPathwayTableJson, ReportAjaxPathDetail, \
                         ReportTfTableJson, ReportAjaxTfDetail, ReportDlFarmJson, ReportCorrelationTableJson, ReportSimilarityJson, \
                         ReportPotentialTargetsJson, ReportTfTrrustTableJson
from food.views import FoodIndex, FoodSearch

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
    url(r'^document/doc(?P<pk>\d+)/report/$', PatientTreatmentPDF.as_view(), name="patient_treatment_pdf"),
    url(r'^document/doc(?P<pk>\d+)/treat(?P<treat_id>.*)/$', PatientTreatmentDetail.as_view(), name="patient_treatment_detail"),
    url(r'^document/doc(?P<pk>\d+)/(?P<sample_name>.*)/$', SampleDetail.as_view(), name="sample_detail"),
    
    
    url(r'^document/ajaxpathdetail/$', AjaxPathDetail.as_view(), name="ajax_path_detail"),
    
    ################### Core App ##############################
    url(r'^calculation-parameters/doc(?P<pk>\d+)/$', CoreSetCalculationParameters.as_view(), name="core_set_calculation_parameters"),
    url(r'^calculation/doc(?P<pk>\d+)/$', CoreCalculation.as_view(), name="core_calculation"),
    
    # OF3 TEST CALCULATIONS
    
    url(r'^of3-calculation-parameters/doc(?P<pk>\d+)/$', OF3CalculationParameters.as_view(), name="of3_calculation_parameters"),
    
    url(r'^test/$', Test.as_view()),
    url(r'^celery/$', Celery.as_view()),
    url(r'^task_status/$', TaskStatus.as_view()),
    
    ################### DataBase App ##############################
    url(r'^db/pathways/(?P<organism>[-\w]+)/(?P<database>[-\w]+)/$', PathwayList.as_view(), name="pathway_list"),
    url(r'^db/pathways/(?P<organism>[-\w]+)/(?P<database>[-\w]+)/[-\w]+/(?P<pk>\d+)/$', PathwayDetail.as_view(), name="pathway_detail"),
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
    
    url(r'^mouse/metabolismpathways/$', MouseMetabolismPathwayList.as_view(), name="mouse_pathway_list"),
    url(r'^mouse/metabolismpathways/[-\w]+/(?P<pk>\d+)/$', MouseMetabolismPathwayDetail.as_view(), name="mouse_pathway_detail"),
    url(r'^mouse/metabolismpathways/search/$', MouseMetabolismPathwayAjaxSearch.as_view(), name="mouse_pathway_ajax_search"),
    
    url(r'^mouse/test/$', MouseTest.as_view(), name="mouse_test"), 

    ################### Medic App ##############################
    url(r'^db/medic/$', MedicNosologyList.as_view(), name="medic_nosology_list"),
    url(r'^medic/generatereport/$', MedicAjaxGenerateReport.as_view(), name="medic_generate_report"),
    url(r'^medic/calculate/$', MedicPatientCalculation.as_view(), name="medic_patient_calculation"),
    url(r'^medic/generatefullreport/$', MedicAjaxGenerateFullReport.as_view(), name="medic_generate_full_report"),
    url(r'^db/medic/[-\w]+/(?P<pk>\d+)/$', MedicNosologyDetail.as_view(), name="medic_nosology_detail"),
    url(r'^db/medic/[-\w]+/[-\w]+/[-\w]+/(?P<pk>\d+)/$', MedicTreatmentDetail.as_view(), name="medic_treatment_detail"),
    
    url(r'^medic/test/$', MedicTest.as_view(), name="medic_test"),
    ################### miRNA App ##############################
    url(r'^mirna-calculation-parameters/doc(?P<pk>\d+)/$', MirnaSetCalculationParameters.as_view(), name="mirna_set_calculation_parameters"),
    
    
    ################### XPN normalization ##############################
    url(r'^shambhala/$', ShambalaForm.as_view(), name="shambala_form"),
    url(r'^shambhala/done/$', ShambalaDone.as_view(), name="shambala_done"),
    url(r'^shambhala/harmony/$', HarmonyForm.as_view(), name="harmony_form"),
    url(r'^shambhala/harmony/done/(.*)/$', HarmonyDone.as_view(), name="harmony_done"),
    url(r'^shambhala/prevfiles/$', HarmonyPrevFiles.as_view(), name="harmony_prevfiles"),
    url(r'^shambhala/breastmodule/$', breastmodule.as_view(), name="breastmodule"),
    
    ################### Different usefull stuff ##############################
    url(r'^utils/path$', ConvertPath.as_view(), name="convert_path"),
    
    
    
    ################### REPORT APP ################################################
    url(r'^report-portal/$', ReportList.as_view(), name="report-index"),
    
    ################### REPORT L'oreal ###############################################
    url(r'^report-portal/report/loreal/$', LorealReport.as_view(), name="loreal-report"),
    url(r'^report-portal/genescatterjson/$', LorealReportGeneScatterJson.as_view(), name="gene_scatter_json"),
    url(r'^report-portal/genetablejson/$', LorealReportGeneTableJson.as_view(), name="gene_table_json"),
    url(r'^report-portal/genedetailjson/$', LorealReportGeneDetailJson.as_view(), name="gene_detail_json"),
    url(r'^report-portal/genesboxplotjson/$', LorealReportGeneBoxplotJson.as_view(), name="gene_boxplot_json"),
    url(r'^report-portal/pathscatterjson/$', LorealReportPathwayScatterJson.as_view(), name="path_scatter_json"),
    url(r'^report-portal/pathwaytablejson/$', LorealReportPathwayTableJson.as_view(), name="pathway_table_json"),
    url(r'^report-portal/report/ajaxpathdetail/$', LorealReportAjaxPathDetail.as_view(), name="report_ajax_path_detail"),
    url(r'^report-portal/report/ajaxpathvenn/$', LorealReportAjaxPathwayVenn.as_view(), name="report_ajax_path_venn"),
    url(r'^report-portal/report/ajaxpathvenntbl/$', LorealReportAjaxPathwayVennTable.as_view(), name="report_ajax_path_venn_tbl"),
    
    ################### REPORT LRL2016 ###############################################
    url(r'^report-portal/report/lrl2016/$', LRLReport.as_view(), name="lrl-report"),
    url(r'^report-portal/lrl-genescatterjson/$', LRLReportGeneScatterJson.as_view(), name="lrl-gene_scatter_json"),
    url(r'^report-portal/lrl-genetablejson/$', LRLReportGeneTableJson.as_view(), name="lrl-gene_table_json"),
    url(r'^report-portal/lrl-genedetailjson/$', LRLReportGeneDetailJson.as_view(), name="lrl-gene_detail_json"),
    url(r'^report-portal/lrl-genevolcanojson/$', LRLGeneVolcanoJson.as_view(), name="lrl-gen-volcano-json"),
    url(r'^report-portal/lrl-genesboxplotjson/$', LRLReportGeneBoxplotJson.as_view(), name="lrl-gene_boxplot_json"),
    url(r'^report-portal/lrl-pathwaytablejson/$', LRLReportPathwayTableJson.as_view(), name="lrl-pathway_table_json"),
    url(r'^report-portal/report/lrl-ajaxpathdetail/$', LRLReportAjaxPathDetail.as_view(), name="lrl-report_ajax_path_detail"),
    url(r'^report-portal/lrl-ajaxpathline/$', LRLReportAjaxPathLine.as_view(), name="lrl-report_ajax_path_line"),
    url(r'^report-portal/lrl-sideefftablejson/$', LRLReportSideEffTableJson.as_view(), name="lrl-sideeff_table_json"),
    ################### REPORT BT ###############################################
    url(r'^report-portal/report/bt/$', BTReport.as_view(), name="bt-report"),
    url(r'^report-portal/bt-genevolcanojson/$', BTGeneVolcanoJson.as_view(), name="bt-gen-volcano-json"),
    url(r'^report-portal/bt-genetablejson/$', BTReportGeneTableJson.as_view(), name="bt-gene_table_json"),
    url(r'^report-portal/bt-genesboxplotjson/$', BTReportGeneBoxplotJson.as_view(), name="bt-gene_boxplot_json"),
    url(r'^report-portal/bt-pathwaytablejson/$', BTReportPathwayTableJson.as_view(), name="pathway_table_json"),
    url(r'^report-portal/report/bt-ajaxpathdetail/$', BTReportAjaxPathDetail.as_view(), name="bt-report_ajax_path_detail"),
    url(r'^report-portal/report/bt-ajaxpathvenn/$', BTReportAjaxPathwayVenn.as_view(), name="bt-report_ajax_path_venn"),
    url(r'^report-portal/report/bt-ajaxpathvenntbl/$', BTReportAjaxPathwayVennTable.as_view(), name="bt-report_ajax_path_venn_tbl"),
    
    ################### REPORT GP ###############################################
    url(r'^report-portal/report/gpcomp/$', GPReport.as_view(), name="gp-report"),
    url(r'^report-portal/gp-pathwaytablejson/$', GPReportPathwayTableJson.as_view(), name="pathway_table_json"),
    url(r'^report-portal/report/gp-ajaxpathvenn/$', GPReportAjaxPathwayVenn.as_view(), name="bt-report_ajax_path_venn"),
    url(r'^report-portal/report/gp-ajaxpathvenntbl/$', GPReportAjaxPathwayVennTable.as_view(), name="bt-report_ajax_path_venn_tbl"),
    url(r'^report-portal/report/gp-ajaxpathdetail/$', GPReportAjaxPathDetail.as_view(), name="bt-report_ajax_path_detail"),
    
    ################### REPORT DEMO ###############################################
    url(r'^report-portal/report/demo/$', DemoReport.as_view(), name="demo-report"),
    url(r'^report-portal/demo/json/$', ReportJson.as_view(), name="report-json"),
    
    ################### REPORT PATH DEMO ###############################################
    url(r'^report-portal/report/path-analysis-demo/$', PathDemoReport.as_view(), name="loreal-report"),
    
    ################### REPORT DEMO 2 (based on BT=report) ###############################################
    url(r'^report-portal/report/demo2/$', Demo2Report.as_view(), name="bt-report"),
    url(r'^report-portal/demo2-genevolcanojson/$', Demo2GeneVolcanoJson.as_view(), name="bt-gen-volcano-json"),
    url(r'^report-portal/demo2-genetablejson/$', Demo2ReportGeneTableJson.as_view(), name="bt-gene_table_json"),
    url(r'^report-portal/demo2-genesboxplotjson/$', Demo2ReportGeneBoxplotJson.as_view(), name="bt-gene_boxplot_json"),
    url(r'^report-portal/demo2-pathwaytablejson/$', Demo2ReportPathwayTableJson.as_view(), name="pathway_table_json"),
    url(r'^report-portal/report/demo2-ajaxpathdetail/$', Demo2ReportAjaxPathDetail.as_view(), name="bt-report_ajax_path_detail"),
    url(r'^report-portal/report/demo2-ajaxpathvenn/$', Demo2ReportAjaxPathwayVenn.as_view(), name="bt-report_ajax_path_venn"),
    url(r'^report-portal/report/demo2-ajaxpathvenntbl/$', Demo2ReportAjaxPathwayVennTable.as_view(), name="bt-report_ajax_path_venn_tbl"),

    ################### REPORT APP ################################################
    url(r'^report-portal/$', ReportList.as_view(), name="report-index"),
    url(r'^report-portal/report/(?P<slug>[-\w]+)/$', ReportDetail.as_view(), name="report-detail"),
    
    url(r'^report-portal/report-genevolcanojson/$', ReportGeneVolcanoJson.as_view(), name="gene-volcano-json"),
    url(r'^report-portal/report-genescatterjson/$', ReportGeneScatterJson.as_view(), name="gene_scatter_json"),
    url(r'^report-portal/report-genetablejson/$', ReportGeneTableJson.as_view(), name="gene_table_json"),
    url(r'^report-portal/report-genetablescatterjson/$', ReportGeneTableScatterJson.as_view(), name="gene_table_scatter_json"),
    url(r'^report-portal/report-genesboxplotjson/$', ReportGeneBoxplotJson.as_view(), name="gene_boxplot_json"),
    url(r'^report-portal/report-genesbarplotjson/$', ReportGeneBarplotJson.as_view(), name="gene_barplot_json"),
    
    url(r'^report-portal/report-ajaxpathvenn/$', ReportAjaxPathwayVenn.as_view(), name="report_ajax_path_venn"),
    url(r'^report-portal/report-ajaxpathvenntbl/$', ReportAjaxPathwayVennTable.as_view(), name="report_ajax_path_venn_tbl"),
    url(r'^report-portal/report-pathwaytablejson/$', ReportPathwayTableJson.as_view(), name="report-pathway_table_json"),
    url(r'^report-portal/report-ajaxpathdetail/$', ReportAjaxPathDetail.as_view(), name="report_ajax_path_detail"),
    
    url(r'^report-portal/report-tftablejson/$', ReportTfTableJson.as_view(), name="tf_table_json"),
    url(r'^report-portal/report-tftrrusttablejson/$', ReportTfTrrustTableJson.as_view(), name="tftrrust_table_json"),
    url(r'^report-portal/report-ajaxtfdetail/$', ReportAjaxTfDetail.as_view(), name="report_ajax_tf_detail"),
    
    url(r'^report-portal/report-deeplearningfarmjson/$', ReportDlFarmJson.as_view(), name="df_farm_json"),
    url(r'^report-portal/report-similaritytablejson/$', ReportSimilarityJson.as_view(), name="df_similarity_json"),
    url(r'^report-portal/report-potenttargetstablejson/$', ReportPotentialTargetsJson.as_view(), name="df_pottargets_json"),    
    
    url(r'^report-portal/report-corrtablejson/$', ReportCorrelationTableJson.as_view(), name="corr_table_json"),
    ################### BLOOD NN ###############################################
    url(r'^nn-blood/$', nnBloodView.as_view(), name="nn-blood"),
    url(r'^nn-blood/result/$', nnBloodResult.as_view(), name="nn-blood"),
    
    ################### FOOD testing mode ###############################################
    url(r'^food/$', FoodIndex.as_view(), name="food_index"),
    url(r'^food/search/$', FoodSearch.as_view(), name="food_search"),

    ################### Housekeeping ###############################################
    url(r'^housekeeping/', include('housekeeping.urls')),
)
