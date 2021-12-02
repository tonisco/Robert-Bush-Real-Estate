from django.shortcuts import render
from .models import Listing
from .form import SearchForm
from django.core.paginator import Paginator


# Create your views here.
def all_listings(request):
    listings = Listing.objects.filter(is_published=True).order_by('-list_date')
    paginator = Paginator(listings, 9)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    form = SearchForm(listing=listings)
    context = {'page_obj': page_obj, 'form': form}
    return render(request, 'listing/listings.html', context=context)
