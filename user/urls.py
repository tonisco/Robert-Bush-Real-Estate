from django.urls import path
from .views import login, logout, register, dashboard,register_admin

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('register/admin/', register_admin, name='register_admin'),
    path('logout/', logout, name='logout'),
    path('dashboard', dashboard, name='dashboard')
]
