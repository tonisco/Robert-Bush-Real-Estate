from django.urls import path
from .views import index, about, agents

urlpatterns = [
    path('about', about, name='about'),
    path('agents', agents, name='agents'),
    path('', index, name='index'),
]
