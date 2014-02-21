from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from users.models import User

@login_required(login_url='/users/login')
def dashboard(request):
    return render(request, 'dashboard.html', {'user':request.user})
