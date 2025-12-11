from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BookingForm, InquiryForm
from .models import Activity, StaffProfile

def book_activity(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                # 1. Save info to Database
                form.save()
                
                # 2. Success Feedback
                messages.success(request, 'Booking Successful! We will contact you shortly to confirm.')
                return redirect('home')
                
            except Exception as e:
                # 3. Handle Conflict (The Model logic we wrote earlier triggers here)
                messages.error(request, f"Booking Failed: {e}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookingForm()

    return render(request, 'operations/book.html', {'form': form})

def contact_us(request):
    """Contact form for customers to reach out to Melissa and staff"""
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            
            # Auto-assign to receptionist (Melissa) if available
            receptionist = StaffProfile.objects.filter(
                role='RECEPTIONIST',
                can_receive_inquiries=True,
                is_active=True
            ).first()
            
            if receptionist:
                inquiry.assigned_to = receptionist.user
            
            inquiry.save()
            messages.success(request, 'Thank you! Your inquiry has been sent. We will get back to you shortly.')
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = InquiryForm()
    
    return render(request, 'operations/contact.html', {'form': form})

def activities_gallery(request):
    """Display all activities with Pinterest gallery"""
    activities = Activity.objects.all()
    return render(request, 'operations/activities.html', {'activities': activities})