from django.shortcuts import render

from .dash_components.simple_example import app

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome to the demo application index.")

def example(request, template_name, **kwargs):
    return render(request, template_name=template_name, context={})
