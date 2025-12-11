from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ClientRegistrationForm, ProfileUpdateForm
from .models import Payment, Message
from operations.models import Booking

def register(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Backyard Adventures.')
            return redirect('client_dashboard')
    else:
        form = ClientRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def client_dashboard(request):
    bookings = Booking.objects.filter(customer_email=request.user.email).order_by('-created_at')
    payments = Payment.objects.filter(booking__customer_email=request.user.email).order_by('-created_at')
    all_messages = Message.objects.filter(recipient=request.user)
    messages_received = all_messages[:5]
    
    context = {
        'bookings': bookings,
        'payments': payments,
        'messages': messages_received,
        'unread_count': all_messages.filter(is_read=False).count()
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def profile(request):
    try:
        profile = request.user.clientprofile
    except:
        from .models import ClientProfile
        profile = ClientProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            profile = form.save()
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile, user=request.user)
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def messages_view(request):
    user_messages = Message.objects.filter(recipient=request.user)
    Message.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return render(request, 'accounts/messages.html', {'messages': user_messages})