from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html', next_page='/accounts/login/'), name='logout'),
    path('dashboard/', views.client_dashboard, name='client_dashboard'),
    path('profile/', views.profile, name='profile'),
    path('messages/', views.messages_view, name='messages'),
]