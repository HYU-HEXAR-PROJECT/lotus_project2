import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http.response import HttpResponseBadRequest
from django.contrib.auth import authenticate, login
from django.views.generic.base import View
from django import forms
from .models import User

class UserValidationForm(forms.Form):
    email = forms.EmailField(max_length=255)
    password = forms.CharField(max_length=128, min_length=4)

class UserLoginView(View):
    template_name = 'login.html'
    error_msg = 'Please check your email or password'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = UserValidationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    self.error_msg = 'This account is disabled'
        else:
            print form.cleaned_data
        return render(request, self.template_name, {'error_msg':self.error_msg})

class UserSignupView(View):
    template_name = 'signup.html'
    error_msg = 'Password cannot be blank.'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        request.POST['password'] = request.POST['password'].strip()
        form = UserValidationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_name = request.POST['user_name'].strip()
            created = False

            try:
                user = User.objects.get(email=email)
            except:
                if len(user_name) > 0:
                    user = User(email=email, user_name=user_name)
                    user.set_password(password)
                    user.save()
                    created = True

            if created:
                user = authenticate(email=email, password=password)
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                if len(user_name) > 0:
                    self.error_msg = 'Email is duplicated! Use another one'
                else:
                    self.error_msg = 'User name cannot be blank'
        return render(request, self.template_name, {'error_msg':self.error_msg})


class DuplicationCheckResponse(HttpResponse):
    def __init__(self, email=None):
        does_email_exist = False
        does_phone_number_exist = False
        output = {'success': True,
                  'message': ''}
        if email:
            does_email_exist = email_exists(email)
            output['email_exists'] = does_email_exist
            if does_email_exist:
                output['message'] = u'Already used email'

        if does_email_exist:
            output['success'] = False
        return super(DuplicationCheckResponse, self).__init__(json.dumps(output))


def check_duplication(request):
    email = request.GET.get('email', '')
    if not email:
        return HttpResponseBadRequest()
    return DuplicationCheckResponse(email=email)
