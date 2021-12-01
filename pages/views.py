from django.shortcuts import render
from listing.form import ListingForm, SearchForm
from listing.models import Listing


# Create your views here.

def index(request):
    listings = Listing.objects.filter(is_published=True).order_by('-list_date')
    context = {'form': SearchForm(listing=listings), 'listings': listings[:6]}
    return render(request, 'pages/index.html', context=context)


def about(request):
    return render(request, 'pages/about.html')
