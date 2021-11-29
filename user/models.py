from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.timezone import now
from .manager import UserManager


def change_image_name(instance, filename):
    new_name = '_'.join([instance.last_name, instance.first_name])
    ext = '.' + filename.split('.')[-1]
    return 'realtor/' + new_name + ext


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    last_name = models.CharField(verbose_name='last name', max_length=255)
    first_name = models.CharField(verbose_name='first name', max_length=255)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    about_me = models.TextField(verbose_name='about', blank=True)
    phone = models.CharField(verbose_name='phone', max_length=20, blank=True)
    photo = models.ImageField(verbose_name='photo', upload_to=change_image_name, blank=True)
    hire_date = models.DateTimeField(default=now, blank=True)
    is_admin = models.BooleanField(default=False, blank=True)
    is_staff = models.BooleanField(default=False, blank=True)
    is_superuser = models.BooleanField(default=False, blank=True)
    is_active = models.BooleanField(default=True, blank=True)

    object = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_name', 'first_name', ]

    def __str__(self):
        return self.email
