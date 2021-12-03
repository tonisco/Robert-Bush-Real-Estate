from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .form import LoginForm, SignUpForm, SignUpAdminForm
from django.contrib import messages, auth

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
        messages.error(request, 'passwords do not match')
        return redirect('register')

    user_exist = User.objects.filter(email=email)
    if user_exist:
        messages.error(request, 'email has already been used')
        return redirect('register')

    user = User(email=email, first_name=first_name, last_name=last_name)
    user.set_password(password)
    return user


def register(request):
    if request.method == 'POST':
        user = check_user(request)
        user.save()
        messages.success(request, 'You have signed up successfully, pls login')
        return redirect('login')

    form = SignUpForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)


def register_admin(request):
    if request.method == 'POST':
        user = check_user(request)
        about_me = request.POST['about_me']
        phone = request.POST['phone']
        photo = request.FILES['photo']
        print(photo)
        user.about_me = about_me
        user.phone = phone
        user.photo = photo
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        messages.success(request, 'You have signed up successfully, pls login')
        return redirect('login')
    form = SignUpAdminForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)


def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect('index')


def dashboard(request):
    return render(request, 'pages/index.html')
