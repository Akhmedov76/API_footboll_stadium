from django.contrib import admin

from .models import FootballField


class FootballFieldAdmin(admin.ModelAdmin):
    """
    Admin panel for FootballField model.
    """
    list_display = ('name', 'stadium', 'image', 'price_per_hour', 'status', 'working_hours_start', 'working_hours_end',)
    search_fields = ('name', 'stadium__name')
    list_filter = ('status', 'stadium', 'created_at')
    ordering = ('-created_at',)


admin.site.register(FootballField, FootballFieldAdmin)
