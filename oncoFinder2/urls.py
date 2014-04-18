# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic.base import  RedirectView

from django.contrib import admin
admin.autodiscover()

from website.views import IndexPage, LoginPage, Logout
from profiles.views import ProfileIndex, SettingsProfile, SettingsBilling, CreateProject, \
                           ProjectDetail, CreateDocument, DocumentDetail

urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': True}),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/media/images/favicon.ico')),
    url(r'^admin/', include(admin.site.urls)),
                       
    ################### Website App ##############################                
    url(r'^$', IndexPage.as_view(), name="website_index"),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'website/login.html'}),
    url(r'^logout$', Logout.as_view(), name="logout"),
    
    
    ################### Profiles App ##############################
    url(r'^user/(?P<slug>[-\w]+)/$', ProfileIndex.as_view(), name="profiles_index"),
    url(r'^settings/profile/$', SettingsProfile.as_view(), name="settings_profile"),
    url(r'^settings/billing/$', SettingsBilling.as_view(), name="settings_billing"),
    
    url(r'^project/new/$', CreateProject.as_view(), name="project_create"),
    url(r'^project/(?P<slug>[-\w]+)/$', ProjectDetail.as_view(), name="project_detail"),
    
    url(r'^document/new/$', CreateDocument.as_view(), name="document_create"),
    url(r'^document/doc(?P<pk>\d+)/$', DocumentDetail.as_view()),

   
)
