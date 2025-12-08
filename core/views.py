from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from operations.models import Activity


def home(request):
    activities = Activity.objects.all()[:6]
    return render(request, 'home.html', {'activities': activities})


def create_admin(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@ba.com', 'password123')
        return HttpResponse("SUCCESS: Superuser 'admin' created! Password is 'password123'")
    return HttpResponse("INFO: Superuser 'admin' already exists.")