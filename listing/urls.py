from django.urls import path
from .views import all_listings, single_listing, search

urlpatterns = [
    path('', all_listings, name='all_listings'),
    path('search', search, name='search'),
    path('<int:listing_id>', single_listing, name='listing')
]
