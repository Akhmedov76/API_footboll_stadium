from django.contrib import admin
from django.utils.html import format_html
from booking.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('field', 'user', 'start_time', 'end_time', 'status', 'created_at')
    list_filter = ('status', 'field', 'created_at')
    search_fields = ('user__username', 'field__name')
    ordering = ('-created_at',)
    date_hierarchy = 'start_time'
    readonly_fields = ('created_at', 'updated_at')

    actions = ['mark_as_confirmed']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.status = 'PENDING'
        obj.save()
