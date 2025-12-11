from django.contrib import admin
from .models import ClientProfile, Payment, Message

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['booking', 'amount', 'status', 'payment_date', 'created_at']
    list_filter = ['status', 'payment_date']
    search_fields = ['booking__customer_name', 'transaction_id']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['subject', 'recipient__username']