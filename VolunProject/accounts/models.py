
from django.db import models
from datetime import time
from django.utils import timezone
    
class HomePageEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='events/')
    show_on_homepage = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return self.title

class AllEvents(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    roles = models.TextField(blank=True)  # comma-separated roles
    tags = models.CharField(max_length=200, blank=True)
    
    @property
    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

    @property
    def role_list(self):
        return [role.strip() for role in self.roles.split(',') if role.strip()]
    
    def __str__(self):
        return self.title
    
class Registration(models.Model):
    event = models.ForeignKey(AllEvents, on_delete=models.CASCADE, related_name='registrations')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=100)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.event.title}"

