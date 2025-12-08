from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.http import HttpResponse

def create_admin(request):
    # Check if the admin already exists to prevent errors
    if not User.objects.filter(username='admin').exists():
        # Create the superuser programmatically
        User.objects.create_superuser('admin', 'admin@ba.com', 'password123')
        return HttpResponse("SUCCESS: Superuser 'admin' created! Password is 'password123'")
    else:
        return HttpResponse("INFO: Superuser 'admin' already exists.")