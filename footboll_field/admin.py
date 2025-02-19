from django.contrib import admin
from .models import FootballField


class FootballFieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'stadium', 'image', 'price_per_hour', 'status', 'created_at')
    search_fields = ('name', 'stadium__name')
    list_filter = ('status', 'stadium', 'created_at')
    ordering = ('-created_at',)


admin.site.register(FootballField, FootballFieldAdmin)
