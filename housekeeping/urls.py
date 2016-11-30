from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.HousekeepingView.as_view()),
    url(r'^ajax/$', views.HousekeepingAjaxView.as_view()),
    url(r'^pathway/$', views.HousekeepingPathwayView.as_view(), name='HousekeepingPathwayView'),
]
