from django.shortcuts import render, get_object_or_404
from .models import Listing
from .form import SearchForm
from django.core.paginator import Paginator
from contact.form import ContactForm


# Create your views here.
def all_listings(request):
    listings = Listing.objects.filter(is_published=True).order_by('-list_date')
    paginator = Paginator(listings, 9)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    form = SearchForm(listing=listings)
    context = {'page_obj': page_obj, 'form': form}
    return render(request, 'listing/listings.html', context=context)


def single_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    form = ''
    if listing:
        form = ContactForm(request=request, listing=listing)
    context = {'listing': listing, 'form': form}
    return render(request, 'listing/listing.html', context)
