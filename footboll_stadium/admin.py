from django.contrib import admin

from footboll_stadium.models import FootballStadium


class FootballFieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'address', 'price_per_hour', 'contact', 'status', 'created_at')
    search_fields = ('name', 'address')
    list_filter = ('price_per_hour',)
    ordering = ('-created_at',)


admin.site.register(FootballStadium, FootballFieldAdmin)
