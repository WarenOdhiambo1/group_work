from django.contrib import admin
from .models import Activity, Booking, Inquiry, StaffProfile

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'price', 'description']
    list_filter = ['type']
    search_fields = ['name', 'description']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'activity', 'date', 'guests', 'is_confirmed', 'created_at']
    list_filter = ['is_confirmed', 'activity__type', 'date']
    search_fields = ['customer_name', 'customer_email']
    date_hierarchy = 'date'

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'status', 'assigned_to', 'created_at']
    list_filter = ['status', 'assigned_to']
    search_fields = ['name', 'email', 'subject']

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'can_receive_inquiries', 'is_active']
    list_filter = ['role', 'is_active']