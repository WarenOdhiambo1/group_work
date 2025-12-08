

# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError

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
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    date = models.DateField()
    is_confirmed = models.BooleanField(default=False)

    def clean(self):
        # SYSTEM LOGIC: Prevent Conflicts
        # "Harry has noticed conflicts" -> This code fixes it.
        existing_bookings = Booking.objects.filter(
            activity=self.activity, 
            date=self.date,
            is_confirmed=True
        )
        if existing_bookings.exists():
            raise ValidationError(f"Conflict! {self.activity.name} is already booked on {self.date}.")

    def save(self, *args, **kwargs):
        self.clean() # Run the check before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_name} - {self.activity} ({self.date})"