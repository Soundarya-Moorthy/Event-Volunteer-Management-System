from django.db import models
from datetime import time

class Volunteer(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    address = models.TextField()
    languages = models.CharField(max_length=100)
    current_status = models.CharField(max_length=20, choices=[('school', 'School'), ('college', 'College'), ('working', 'Working'), ('other', 'Other')])
    preferred_days = models.CharField(max_length=100)
    preferred_time_slots = models.CharField(max_length=100)
    
    # Optional fields
    specific_dates = models.CharField(max_length=100, blank=True, null=True)
    has_experience = models.BooleanField(default=False)
    experience_details = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"