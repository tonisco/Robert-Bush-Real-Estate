from django.urls import path
from .views import index, about, agents, agent

urlpatterns = [
    path('about', about, name='about'),
    path('agents', agents, name='agents'),
    path('agent/<int:agent_id>', agent, name='agent'),
    path('', index, name='index'),
]
