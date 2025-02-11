from django.contrib import admin
from django.utils.html import format_html
from booking.models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('field', 'user', 'start_time', 'end_time', 'colored_status', 'created_at')
    list_filter = ('status', 'field', 'created_at')
    search_fields = ('user__username', 'field__name')
    ordering = ('-created_at',)
    date_hierarchy = 'start_time'
    readonly_fields = ('created_at', 'updated_at')

    actions = ['mark_as_confirmed']

    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='CONFIRMED')

    mark_as_confirmed.short_description = "Mark selected bookings as Confirmed"

    def colored_status(self, obj):
        colors = {
            'PENDING': 'orange',
            'CONFIRMED': 'green',
            'CANCELLED': 'red',
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.status, 'black'), obj.get_status_display()
        )

    colored_status.admin_order_field = 'status'
    colored_status.short_description = 'Status'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.status = 'PENDING'
        obj.save()
