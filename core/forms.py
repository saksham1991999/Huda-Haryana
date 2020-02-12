from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from . import models

class propertyForm(forms.ModelForm):
    class Meta:
        model = models.property
        exclude = ['verified', 'views', 'owner', 'visible', 'dateadded']
        labels = {
            'type': _('Select Type'),
            'property_name': _('Property Name'),
            'city': _('City'),
            'bedrooms': _('No of Bedrooms'),
            'bathrooms': _('No of Bathrooms'),
            'rooms': _('No of Rooms'),
            'construction_status': _('Construction Status (Optional)'),
            'available_from': _('Available from Date (YYYY-MM-DD) (Optional)'),
            'price_sq': _('Price per sq m (Optional)'),
            'total_price': _('Total Price'),
            'additional_features': _('Additional Features'),
            'image': _('Main Image'),
            'label': _('Label (Optional)'),
            'features': _('Features (Multi-Select)'),
        }
        widgets = {
            'features': forms.SelectMultiple(attrs={'rows':'4'})
        }

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