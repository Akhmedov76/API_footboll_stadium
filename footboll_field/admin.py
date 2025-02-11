from django.contrib import admin

from footboll_field.models import FootballField


class FootballFieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'price_per_hour', 'created_at')
    search_fields = ('name', 'address')
    list_filter = ('price_per_hour',)
    ordering = ('-created_at',)


admin.site.register(FootballField, FootballFieldAdmin)
