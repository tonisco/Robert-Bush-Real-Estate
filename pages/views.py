from django.shortcuts import render
from listing.form import SearchForm
from listing.models import Listing
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q

# from user.models import User

User = get_user_model()


# Create your views here.

def index(request):
    listings = Listing.objects.filter(is_published=True).order_by('-list_date')
    context = {'form': SearchForm(listing=listings), 'listings': listings[:6]}
    return render(request, 'pages/index.html', context=context)


def about(request):
    return render(request, 'pages/about.html')


def agents(request):
    user = User.objects.filter(~Q(email='t@m.com')).order_by('-hire_date')
    paginator = Paginator(user, 9)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = {'page_obj': page_obj}
    return render(request, 'pages/realtors.html', context=context)
