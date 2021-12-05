from django.shortcuts import render, redirect
import os
from django.contrib.auth import get_user_model
from .form import LoginForm, SignUpForm, SignUpAdminForm, UserEditForm
from django.contrib import messages, auth
from contact.models import Contact
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from listing.models import Listing
from listing.form import ListingForm
from django.core.files.storage import default_storage

User = get_user_model()


# Create your views here.
def login(request):
    form = LoginForm()
    context = {'form': form}
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Wrong email or password')
            return redirect('login')
    return render(request, 'users/login.html', context)


def check_user(request):
    email = request.POST['email']
    password = request.POST['password1']
    confirm_password = request.POST['password2']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    if password != confirm_password:
        user = 'Passwords do not match'
        return user

    user_exist = User.objects.filter(email=email)
    if user_exist:
        user = 'Email has already been used'
        return user

    user = User(email=email, first_name=first_name, last_name=last_name)
    user.set_password(password)
    return user


def register(request):
    if request.method == 'POST':
        user = check_user(request)
        if isinstance(user, User):
            user.save()
            messages.success(request, 'You have signed up successfully, pls login')
            return redirect('login')
        else:
            messages.error(request, user)
            return redirect('register')

    form = SignUpForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)


def register_admin(request):
    if request.method == 'POST':
        user = check_user(request)
        if isinstance(user, User):
            about_me = request.POST['about_me']
            phone = request.POST['phone']
            photo = request.FILES['photo']
            user.about_me = about_me
            user.phone = phone
            user.photo = photo
            user.is_admin = True
            user.is_staff = True
            user.is_superuser = True
            user.save()
            messages.success(request, 'You have signed up successfully, pls login')
            return redirect('login')
        else:
            messages.error(request, user)
            return redirect('register')
    form = SignUpAdminForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)


def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect('index')


def dashboard(request):
    user = auth.get_user(request)
    if user.is_authenticated:
        if user.is_superuser:
            listings = Contact.objects.filter(realtor=user.email).order_by('-contact_date')
        else:
            listings = Contact.objects.filter(user_id=user.id).order_by('-contact_date')
        context = {'listings': listings}
        return render(request, 'users/dashboard.html', context)
    else:
        return redirect('index')


def settings(request):
    user = auth.get_user(request)
    if user.is_superuser and user.is_authenticated:
        if request.method == 'POST':
            user.email = request.POST['email']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.phone = request.POST['phone']
            user.about_me = request.POST['about_me']
            if 'photo' in request.FILES and request.FILES != 0:
                os.remove(user.photo.path)
                user.photo = request.FILES['photo']
            user.save()
            messages.success(request, 'Edits have been saved')
        form = UserEditForm(user=user)
        context = {'form': form}
        return render(request, 'users/settings.html', context)
    else:
        return redirect('index')


def agent_listing(request):
    user = auth.get_user(request)
    if user.is_superuser and user.is_authenticated:
        listings = Listing.objects.filter(realtor_id=user.id).order_by('-list_date')
        context = {}
        if listings.count() > 0:
            paginator = Paginator(listings, 9)
            page = request.GET.get('page')
            try:
                page_obj = paginator.get_page(page)
            except PageNotAnInteger:
                page_obj = paginator.get_page(1)
            except EmptyPage:
                page_obj = paginator.get_page(paginator.num_pages)
            context = {'page_obj': page_obj}

        return render(request, 'users/agent_listing.html', context)
    else:
        return redirect('index')


def listing_details(request, listing=None):
    if not listing:
        listing = Listing()
    user = auth.get_user(request)
    listing.realtor = user
    listing.title = request.POST['title']
    listing.address = request.POST['address']
    listing.city = request.POST['city']
    listing.state = request.POST['state']
    listing.offer_type = request.POST['offer_type']
    listing.zipcode = request.POST['zipcode']
    listing.price = request.POST['price']
    listing.bedrooms = request.POST['bedrooms']
    listing.baths = request.POST['baths']
    listing.sqft = request.POST['sqft']
    listing.garage = request.POST['garage']
    listing.pool = request.POST['pool']
    listing.description = request.POST['description']
    listing.list_date = request.POST['list_date']
    listing.is_published = request.POST['is_published'] == 'on'
    return listing


def remove_image(image):
    if image != '' and os.path.exists(image.path):
        os.remove(image.path)


def image_to_remove(request, listing):
    if 'photo_main-clear' in request.POST:
        remove_image(listing.photo_main)
        listing.photo_main = ''
    if 'photo_1-clear' in request.POST:
        remove_image(listing.photo_1)
        listing.photo_1 = ''
    if 'photo_2-clear' in request.POST:
        remove_image(listing.photo_2)
        listing.photo_2 = ''
    if 'photo_3-clear' in request.POST:
        remove_image(listing.photo_3)
        listing.photo_3 = ''
    if 'photo_4-clear' in request.POST:
        remove_image(listing.photo_4)
        listing.photo_4 = ''
    if 'photo_5-clear' in request.POST:
        remove_image(listing.photo_5)
        listing.photo_5 = ''

    return listing


def listing_images(request, listing):
    if 'photo_main' in request.FILES:
        remove_image(listing.photo_main)
        listing.photo_main = request.FILES['photo_main']
    if 'photo_1' in request.FILES:
        remove_image(listing.photo_1)
        listing.photo_1 = request.FILES['photo_1']
    if 'photo_2' in request.FILES:
        remove_image(listing.photo_2)
        listing.photo_2 = request.FILES['photo_2']
    if 'photo_3' in request.FILES:
        remove_image(listing.photo_3)
        listing.photo_3 = request.FILES['photo_3']
    if 'photo_4' in request.FILES:
        remove_image(listing.photo_4)
        listing.photo_4 = request.FILES['photo_4']
    if 'photo_5' in request.FILES:
        remove_image(listing.photo_5)
        listing.photo_5 = request.FILES['photo_5']
    return listing


def listing_edit(request, listing_id):
    user = auth.get_user(request)
    if user.is_superuser and user.is_authenticated:
        listing = Listing.objects.get(id=listing_id)
        if user != listing.realtor:
            return redirect('agent_listing')
        if request.method == 'POST':
            listing = listing_details(request, listing)
            listing = image_to_remove(request, listing)
            if request.FILES != 0:
                listing = listing_images(request, listing)
            listing.save()
            messages.success(request, 'Listing has been saved')
            return redirect('agent_listing')

        form = ListingForm(request=request, listing=listing)
        context = {'form': form, 'listing': listing}
        return render(request, 'users/listing_edit.html', context)
    else:
        return redirect('index')


def listing_create(request):
    user = auth.get_user(request)
    if user.is_superuser and user.is_authenticated:
        if request.method == 'POST':
            listing = listing_details(request)
            if request.FILES != 0:
                listing = listing_images(request, listing)
            listing.save()
            messages.success(request, 'Listing has been saved')
            return redirect('agent_listing')

        form = ListingForm(request=request)
        context = {'form': form}
        return render(request, 'users/listing_edit.html', context)
    else:
        return redirect('index')


def listing_delete(request, listing_id):
    user = auth.get_user(request)
    if user.is_superuser and user.is_authenticated:
        listing = Listing.objects.get(id=listing_id)
        remove_image(listing.photo_main)
        remove_image(listing.photo_1)
        remove_image(listing.photo_2)
        remove_image(listing.photo_3)
        remove_image(listing.photo_4)
        remove_image(listing.photo_5)

        listing.delete()
        messages.success(request, 'Listing successfully deleted')
        return redirect('agent_listing')
    else:
        redirect('index')
