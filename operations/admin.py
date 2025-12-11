from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Activity, Booking, Inquiry, StaffProfile

# 1. ACTIVITY MANAGEMENT (Adding Items)
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price')
    search_fields = ('name', 'description')
    list_filter = ('type',)

# 2. BOOKING MANAGEMENT (The "Binder" Replacement)
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    # What columns to see in the list
    list_display = ('customer_name', 'customer_email', 'activity', 'date', 'time', 'guests', 'is_confirmed', 'created_at')
    
    # Add filters so Melissa can run her "Morning Report" (Filter by Date)
    list_filter = ('date', 'is_confirmed', 'activity', 'created_at')
    
    # Allow searching by customer name
    search_fields = ('customer_name', 'customer_email', 'customer_phone')
    
    # Allow editable list for quick confirmations
    list_editable = ('is_confirmed',)
    
    date_hierarchy = 'date'
    ordering = ('-date', '-time')

# 3. INQUIRY MANAGEMENT (Customer Contact System)
@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'assigned_to', 'created_at')
    list_filter = ('status', 'created_at', 'assigned_to')
    search_fields = ('name', 'email', 'subject', 'message')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_editable = ('status',)
    
    def save_model(self, request, obj, form, change):
        # Auto-assign to Melissa or first staff member with receptionist role if not assigned
        if not obj.assigned_to:
            staff_members = StaffProfile.objects.filter(
                role='RECEPTIONIST', 
                can_receive_inquiries=True,
                is_active=True
            ).first()
            if staff_members:
                obj.assigned_to = staff_members.user
        super().save_model(request, obj, form, change)

# 4. STAFF PROFILE MANAGEMENT (User like Melissa)
@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'can_receive_inquiries', 'is_active')
    list_filter = ('role', 'can_receive_inquiries', 'is_active')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone')
    list_editable = ('can_receive_inquiries', 'is_active')