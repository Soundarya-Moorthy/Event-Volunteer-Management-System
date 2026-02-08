
from django import forms
from .models import Volunteer
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        has_experience = cleaned_data.get('has_experience')
        experience_details = cleaned_data.get('experience_details')

        if has_experience and not experience_details:
            self.add_error('experience_details', 'Please provide details about your experience.')
