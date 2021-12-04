from django.shortcuts import render
from listing.form import SearchForm
from listing.models import Listing
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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
    try:
        page_obj = paginator.get_page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context = {'page_obj': page_obj}
    return render(request, 'pages/realtors.html', context=context)


def agent(request, agent_id):
    agent = User.objects.get(id=agent_id)
    agent_listing = Listing.objects.filter(realtor_id=agent_id).order_by('-list_date')
    paginator = Paginator(agent_listing, 6)
    page_num = request.GET.get('page')
    print(agent)
    try:
        page_obj = paginator.get_page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context = {'agent': agent, 'page_obj': page_obj}
    return render(request, 'pages/realtor.html', context)
