from django.contrib import admin

from booking.models import Booking


class BookingAdmin(admin.ModelAdmin):
    list_display = ('field', 'user', 'start_time', 'end_time', 'status', 'created_at')
    list_filter = ('status', 'field', 'created_at')
    search_fields = ('user__username', 'field__name')
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.status = 'PENDING'
        obj.save()


admin.site.register(Booking, BookingAdmin)
