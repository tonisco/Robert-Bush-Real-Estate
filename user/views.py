from django.shortcuts import render, redirect
import os
from django.contrib.auth import get_user_model
from .form import LoginForm, SignUpForm, SignUpAdminForm, UserEditForm
from .models import User as UserModel
from django.contrib import messages, auth
from contact.models import Contact
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from listing.models import Listing
from listing.form import ListingForm

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
            messages.error(request, 'wrong email or password')
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
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            phone = request.POST['phone']
            about_me = request.POST['about_me']
            if 'photo' in request.FILES:
                photo = request.FILES['photo']
                print(user.photo)
                os.remove(user.photo)
                user = user(id=user.id, email=email, first_name=first_name, last_name=last_name, phone=phone,
                            about_me=about_me, photo=photo)
            else:
                user = user(id=user.id, email=email, first_name=first_name, last_name=last_name, phone=phone,
                            about_me=about_me)
            user.save()
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


def listing_edit(request):
    user = auth.get_user(request)
    if user.is_superuser and user.is_authenticated:
        form = ListingForm(request=request)
        context = {'form': form}
        return render(request, 'users/listing_edit.html', context)
    else:
        return redirect('index')
