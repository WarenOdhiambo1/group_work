from django.urls import path
from . import views

urlpatterns = [
    # CHANGE THIS LINE
    # We use an empty string '' because the prefix 'dashboard/' 
    # is already handled in the main config file.
    path('', views.dashboard, name='dashboard'),
]