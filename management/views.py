from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from operations.models import Activity, Booking, Inquiry, StaffProfile
from accounts.models import ClientProfile, Payment, Message
from django.contrib.auth.models import User
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

def is_manager(user):
    return user.is_staff and hasattr(user, 'staff_profile') and user.staff_profile.role == 'MANAGER'

def is_melissa(user):
    return user.is_staff and hasattr(user, 'staff_profile') and user.staff_profile.role == 'RECEPTIONIST'

@login_required
@user_passes_test(is_manager)
def manager_dashboard(request):
    # Get analytics data
    total_clients = ClientProfile.objects.filter(user__is_staff=False).count()
    total_bookings = Booking.objects.count()
    confirmed_bookings = Booking.objects.filter(is_confirmed=True).count()
    total_revenue = Payment.objects.filter(status='PAID').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Recent activity
    recent_bookings = Booking.objects.order_by('-created_at')[:10]
    recent_payments = Payment.objects.order_by('-created_at')[:10]
    all_clients = ClientProfile.objects.filter(user__is_staff=False)[:10]
    
    context = {
        'total_clients': total_clients,
        'total_bookings': total_bookings,
        'confirmed_bookings': confirmed_bookings,
        'total_revenue': total_revenue,
        'recent_bookings': recent_bookings,
        'recent_payments': recent_payments,
        'all_clients': all_clients,
    }
    return render(request, 'management/manager_dashboard.html', context)

@login_required
@user_passes_test(is_manager)
def analytics_report(request):
    # Generate analytics charts
    chart_data = generate_analytics_charts()
    return render(request, 'management/analytics.html', {'charts': chart_data})

@login_required
@user_passes_test(is_melissa)
def melissa_dashboard(request):
    # Melissa's customer service dashboard
    pending_inquiries = Inquiry.objects.filter(status='NEW')
    my_inquiries = Inquiry.objects.filter(assigned_to=request.user)
    pending_payments = Payment.objects.filter(status='PENDING')
    
    context = {
        'pending_inquiries': pending_inquiries,
        'my_inquiries': my_inquiries,
        'pending_payments': pending_payments,
    }
    return render(request, 'management/melissa_dashboard.html', context)

@login_required
@user_passes_test(is_melissa)
def update_payment_status(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        payment.status = status
        if status == 'PAID':
            payment.payment_date = timezone.now()
        payment.save()
        messages.success(request, f'Payment status updated to {status}')
    return redirect('melissa_dashboard')

@login_required
@user_passes_test(is_melissa)
def send_message_to_client(request, client_id):
    client = get_object_or_404(User, id=client_id)
    if request.method == 'POST':
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        Message.objects.create(
            sender=request.user,
            recipient=client,
            subject=subject,
            content=content
        )
        messages.success(request, f'Message sent to {client.get_full_name()}')
    return redirect('melissa_dashboard')

def generate_analytics_charts():
    # Revenue over time
    payments = Payment.objects.filter(status='PAID').values('payment_date__date').annotate(revenue=Sum('amount'))
    df_revenue = pd.DataFrame(list(payments))
    
    # Most popular activities
    bookings = Booking.objects.values('activity__name').annotate(count=Count('id'))
    df_activities = pd.DataFrame(list(bookings))
    
    charts = {}
    
    # Revenue chart
    if not df_revenue.empty:
        plt.figure(figsize=(10, 6))
        plt.plot(df_revenue['payment_date__date'], df_revenue['revenue'])
        plt.title('Revenue Over Time')
        plt.xlabel('Date')
        plt.ylabel('Revenue ($)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        charts['revenue'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
    
    # Activity popularity chart
    if not df_activities.empty:
        plt.figure(figsize=(10, 6))
        plt.bar(df_activities['activity__name'], df_activities['count'])
        plt.title('Most Popular Activities')
        plt.xlabel('Activity')
        plt.ylabel('Bookings')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        charts['activities'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
    
    return charts