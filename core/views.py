from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from operations.models import Activity
from operations.utils import get_pinterest_gallery_items


def home(request):
    activities = Activity.objects.all()[:6]
    gallery_items = get_pinterest_gallery_items()
    return render(request, 'home.html', {
        'activities': activities,
        'gallery_items': gallery_items
    })


def create_admin(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@ba.com', 'password123')
        return HttpResponse("SUCCESS: Superuser 'admin' created! Password is 'password123'")
    return HttpResponse("INFO: Superuser 'admin' already exists.")