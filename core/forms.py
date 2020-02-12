from django import forms

from . import models

class propertyForm(forms.ModelForm):
    class Meta:
        model = models.property
        exclude = ['verified', 'views', 'owner', 'visible']

class contactForm(forms.ModelForm):
    class Meta:
        model = models.contact
        fields = [
            'name',
            'email',
            'subject',
            'message',
        ]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name']