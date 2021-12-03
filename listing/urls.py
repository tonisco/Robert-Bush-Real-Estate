from django.urls import path
from .views import all_listings, single_listing

urlpatterns = [
    path('', all_listings, name='all_listings'),
    path('<int:listing_id>', single_listing, name='listing')
]
