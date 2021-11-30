from django.shortcuts import render
from listing.form import ListingForm, SearchForm
from listing.models import Listing


# Create your views here.

def index(request):
    listings = Listing.objects.all()
    context = {'form': SearchForm(listing=listings), 'listings': listings[:9]}
    return render(request, 'pages/index.html', context=context)
