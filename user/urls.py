from django.urls import path
from .views import login, logout, register, dashboard, register_admin, agent_listing, listing_edit, settings

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('register/admin/', register_admin, name='register_admin'),
    path('logout/', logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('listing/', agent_listing, name='agent_listing'),
    path('settings/', settings, name='settings'),
    path('listing/edit', listing_edit, name='listing_edit')
]
