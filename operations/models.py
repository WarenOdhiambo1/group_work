

# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone

# 1. The Inventory (Tours & Rentals)
class Activity(models.Model):
    ACTIVITY_TYPES = (('TOUR', 'Guided Tour'), ('RENTAL', 'Equipment Rental'))
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=ACTIVITY_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image_url = models.URLField(max_length=500, blank=True)

    def __str__(self):
        return self.name

# 2. The Booking System (Replacing the "Binder")
class Booking(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, blank=True, default='')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    guests = models.IntegerField(default=1)
    is_confirmed = models.BooleanField(default=False)
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def clean(self):
        # SYSTEM LOGIC: Prevent Conflicts
        # "Harry has noticed conflicts" -> This code fixes it.
        existing_bookings = Booking.objects.filter(
            activity=self.activity, 
            date=self.date,
            is_confirmed=True
        )
        if self.pk:  # If updating existing booking, exclude itself
            existing_bookings = existing_bookings.exclude(pk=self.pk)
        
        if existing_bookings.exists():
            raise ValidationError(f"Conflict! {self.activity.name} is already booked on {self.date}.")

    def save(self, *args, **kwargs):
        self.clean() # Run the check before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_name} - {self.activity} ({self.date})"

# 3. Inquiry System - For customers to contact Melissa
class Inquiry(models.Model):
    STATUS_CHOICES = (
        ('NEW', 'New'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    )
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_inquiries')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Inquiries'
    
    def __str__(self):
        return f"{self.name} - {self.subject}"

# 4. User Profile Extension for Staff Members like Melissa
class StaffProfile(models.Model):
    ROLE_CHOICES = (
        ('RECEPTIONIST', 'Receptionist'),
        ('TOUR_GUIDE', 'Tour Guide'),
        ('MANAGER', 'Manager'),
        ('ADMIN', 'Admin'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    can_receive_inquiries = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.role}"