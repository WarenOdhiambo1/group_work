from django.urls import path
from . import views

urlpatterns = [
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('analytics/', views.analytics_report, name='analytics_report'),
    path('melissa/', views.melissa_dashboard, name='melissa_dashboard'),
    path('payment/<int:payment_id>/update/', views.update_payment_status, name='update_payment_status'),
    path('message/<int:client_id>/', views.send_message_to_client, name='send_message_to_client'),
]