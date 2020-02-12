from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime

type_choices = (
    ('B', 'Buy'),
    ('S', 'Sell'),
    ('R', 'Rent'),
)

construction_choices = (
    ('RM', 'Ready to Move'),
    ('UC', 'Under Construction'),
)


class User(AbstractUser):
    is_agent = models.BooleanField(default=False)
    mobile = models.CharField(max_length=10)
    mobile_verified = models.BooleanField(default=False)
    profile_pic = models.ImageField(blank = True, null = True)

    def __str__(self):
        return self.username

class features(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title.capitalize()

class property(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(choices=type_choices, max_length=1)
    property_name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    construction_status = models.CharField(choices=construction_choices, max_length=2, blank=True, null = True)
    available_from = models.DateField(blank=True, null=True)
    price_sq = models.FloatField(blank=True, null=True)
    total_price = models.FloatField()
    additional_features = models.TextField(blank = True, null = True)
    image = models.ImageField()
    visible = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    label = models.CharField(max_length = 10, null=True, blank=True)
    dateadded = models.DateField(auto_now_add=True)
    rooms = models.IntegerField()
    features = models.ManyToManyField(features)

    def __str__(self):
        return self.property_name

    class Meta:
        verbose_name_plural = 'Properties'

    # def get_label(self):
    #     if self.label:
    #         return self.label
    #     else:
    #         return None



class images(models.Model):
    image = models.ImageField()
    property = models.ForeignKey(property, on_delete=models.CASCADE)

    def __str__(self):
        return self.property.property_name

    class Meta:
        verbose_name_plural = 'Images'

class videos(models.Model):
    video = models.FileField(upload_to='videos/')
    property = models.ForeignKey(property, on_delete=models.CASCADE)

    def __str__(self):
        return self.property.property_name

    class Meta:
        verbose_name_plural = 'Videos'

class agent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    image = models.ImageField()

class Compare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    properties = models.ManyToManyField(property)

    def get_properties(self):
        properties_compare = self.propeerties.all()[:4]
        return properties_compare

    def __str__(self):
        return self.user.username

class bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    properties = models.ManyToManyField(property)

    def __str__(self):
        return self.user.username

class contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.name

