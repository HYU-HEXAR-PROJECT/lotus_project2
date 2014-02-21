from django.conf.urls import patterns, url

from .views import dashboard

urlpatterns = patterns('',
    url(r'^$', dashboard, name='dashboard'),
)
