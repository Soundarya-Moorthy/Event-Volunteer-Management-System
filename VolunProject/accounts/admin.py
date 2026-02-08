from django.contrib import admin
from .models import HomePageEvent
from .models import AllEvents

admin.site.register(HomePageEvent)

@admin.register(AllEvents)
class AllEventsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location')
    search_fields = ('title', 'location', 'tags')