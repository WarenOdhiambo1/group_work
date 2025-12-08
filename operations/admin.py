from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Activity, Booking

# 1. ACTIVITY MANAGEMENT (Adding Items)
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price')
    search_fields = ('name',)
    list_filter = ('type',)

# 2. BOOKING MANAGEMENT (The "Binder" Replacement)
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    # What columns to see in the list
    list_display = ('customer_name', 'activity', 'date', 'is_confirmed')
    
    # Add filters so Melissa can run her "Morning Report" (Filter by Date)
    list_filter = ('date', 'is_confirmed', 'activity')
    
    # Allow searching by customer name
    search_fields = ('customer_name', 'customer_email')
    
    # Allow editable list for quick confirmations
    list_editable = ('is_confirmed',)