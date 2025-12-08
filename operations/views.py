from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BookingForm

def book_activity(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                # 1. Save info to Database
                form.save()
                
                # 2. Success Feedback
                messages.success(request, 'Registration Successful! Your booking is confirmed.')
                return redirect('home')
                
            except Exception as e:
                # 3. Handle Conflict (The Model logic we wrote earlier triggers here)
                messages.error(request, f"Booking Failed: {e}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookingForm()

    return render(request, 'operations/book.html', {'form': form})