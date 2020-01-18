from django.db import models


type_choices = (
    ('B', 'Buy'),
    ('S', 'Sell'),
    ('R', 'Rent'),
)

construction_choices = (
    ('RM', 'Ready to Move'),
    ('UC', 'Under Construction'),
)

# Create your models here.
class property(models.Model):
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

    def __str__(self):
        return self.property_name

    class Meta:
        verbose_name_plural = 'Properties'

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