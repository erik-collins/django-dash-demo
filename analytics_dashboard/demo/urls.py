from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('example', views.example, {'template_name': 'example/index.html'}, name='example'),
]