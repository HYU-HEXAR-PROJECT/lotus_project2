from django.conf.urls import patterns, url

from .views import UserLoginView, UserSignupView

urlpatterns = patterns('',
        url(r'^login$', UserLoginView.as_view()),
        url(r'^signup$', UserSignupView.as_view()),
)
