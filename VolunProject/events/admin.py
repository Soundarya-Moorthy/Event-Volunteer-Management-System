from django.contrib import admin
from accounts.models import Registration
from .models import Volunteer
from .models import ContactMessage

admin.site.register(Volunteer)

#@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'role', 'event', 'registered_at')
    list_filter = ('event', 'role')
    search_fields = ('name', 'email', 'phone')

class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'current_status', 'has_experience')
    search_fields = ('full_name', 'email', 'languages_known')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')
    search_fields = ('name', 'email')