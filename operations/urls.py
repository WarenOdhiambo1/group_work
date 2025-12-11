from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_activity, name='book_activity'),
    path('contact/', views.contact_us, name='contact_us'),
    path('activities/', views.activities_gallery, name='activities_gallery'),
]