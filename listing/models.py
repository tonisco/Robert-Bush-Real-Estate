from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from .choices import offer_choices
from random import randint

user = get_user_model()


def random_name():
    name = ''
    letters = '12345667890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i in range(12):
        index = randint(0, len(letters) - 1)
        name += letters[index]
    return name


def change_image_name(instance, filename):
    folder = '_'.join(instance.title.split(' '))
    new_name = random_name()
    ext = '.' + filename.split('.')[-1]
    return 'listing/' + folder + '/' + new_name + ext


# Create your models here.
class Listing(models.Model):
    realtor = models.ForeignKey(user, models.CASCADE)
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    offer_type = models.CharField(max_length=100, choices=offer_choices)
    zipcode = models.CharField(max_length=20)
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    sqft = models.IntegerField()
    garage = models.IntegerField()
    pool = models.IntegerField()
    description = models.TextField(max_length=200)
    photo_main = models.ImageField(upload_to=change_image_name)
    photo_1 = models.ImageField(upload_to=change_image_name, blank=True)
    photo_2 = models.ImageField(upload_to=change_image_name, blank=True)
    photo_3 = models.ImageField(upload_to=change_image_name, blank=True)
    photo_4 = models.ImageField(upload_to=change_image_name, blank=True)
    photo_5 = models.ImageField(upload_to=change_image_name, blank=True)
    is_published = models.BooleanField(default=False, blank=True)
    list_date = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return self.title
