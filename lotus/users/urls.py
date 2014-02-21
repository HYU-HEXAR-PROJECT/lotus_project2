from django.conf.urls import patterns, url

from .views import UserView

urlpatterns = patterns('',
        url(r'^login$', UserView.as_view()),
)
