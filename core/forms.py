from django import forms

from . import models

class propertyForm(forms.ModelForm):
    class Meta:
        model = models.property
        fields = [
        'type', 'property_name', 'city' , 'bedrooms', 'bathrooms', 'construction_status','available_from',
        'price_sq',
        'total_price',
        'additional_features',
        'image'
        ]

class contactForm(forms.ModelForm):
    class Meta:
        model = models.contact
        fields = [
            'name',
            'email',
            'subject',
            'message',
        ]