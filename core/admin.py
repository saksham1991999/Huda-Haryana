from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.property)
admin.site.register(models.images)
admin.site.register(models.videos)
admin.site.register(models.features)
admin.site.register(models.contact)
admin.site.register(models.bookmark)
admin.site.register(models.agent)