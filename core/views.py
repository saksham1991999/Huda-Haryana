from django.shortcuts import render
from . import models
# Create your views here.
def HomeView(request):
    properties = models.property.objects.all()[:4]

    context = {
        'properties':properties,
    }
    return render(request, 'index.html', context)