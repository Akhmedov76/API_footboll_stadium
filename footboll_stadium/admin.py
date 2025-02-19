from django.contrib import admin

from footboll_stadium.models import FootballStadium


class FootballStadiumAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'address', 'contact', 'status', 'created_at')
    search_fields = ('name', 'address')
    list_filter = ('address', 'created_at')
    ordering = ('-created_at',)


admin.site.register(FootballStadium, FootballStadiumAdmin)
