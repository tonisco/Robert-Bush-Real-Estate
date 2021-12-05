from django.shortcuts import render, get_object_or_404, redirect
from .models import Listing
from .form import SearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from contact.form import ContactForm


# Create your views here.
def all_listings(request):
    listings = Listing.objects.filter(is_published=True).order_by('-list_date')
    if listings.count() > 0:
        paginator = Paginator(listings, 9)
        page_num = request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

    form = SearchForm(listing=listings)
    context = {'page_obj': page_obj, 'form': form}
    return render(request, 'listing/listings.html', context)


def single_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    form = ''
    if listing:
        form = ContactForm(request=request, listing=listing)
    context = {'listing': listing, 'form': form}
    return render(request, 'listing/listing.html', context)


def search(request):
    if request.method == 'POST':
        listings = Listing.objects.filter(is_published=True)
        searches = {}
        if 'offer_type' in request.POST and request.POST['offer_type']:
            listings = listings.filter(offer_type=request.POST['offer_type'])
            searches['offer_type'] = request.POST['offer_type']
        if 'state' in request.POST and request.POST['state']:
            listings = listings.filter(state=request.POST['state'])
            searches['state'] = request.POST['state']
        if 'bedrooms' in request.POST and request.POST['bedrooms']:
            listings = listings.filter(bedrooms__gte=request.POST['bedrooms'])
            searches['bedrooms'] = request.POST['bedrooms']
        if 'baths' in request.POST and request.POST['baths']:
            listings = listings.filter(baths__gte=request.POST['baths'])
            searches['baths'] = request.POST['baths']
        if 'sqft' in request.POST and request.POST['sqft']:
            listings = listings.filter(sqft__gte=request.POST['sqft'])
            searches['sqft'] = request.POST['sqft']
        if 'price' in request.POST and request.POST['price']:
            listings = listings.filter(price__lte=request.POST['price'])
            searches['price'] = request.POST['price']
        paginator = Paginator(listings.order_by('-list_date'), 9)
        page = request.GET.get('page')
        try:
            page_obj = paginator.get_page(page)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)
        form = SearchForm(listing=listings, searches=searches)
        context = {'page_obj': page_obj, 'form': form, 'searched': True}
        return render(request, 'listing/listings.html', context)
    else:
        return redirect('all_listings')
