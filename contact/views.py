from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages
from django.core.mail import send_mail
from listing.models import Listing


# Create your views here.

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        name = request.POST['name']
        listing = request.POST['listing']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']

        details = Listing.objects.filter(id=listing_id)

        new_contact = Contact(listing_id=listing_id, name=name, listing=listing,
                              email=email, phone=phone, message=message, user_id=user_id)
        new_contact.save()
        messages.success(request=request,
                         message='Your enquiry on the property has been made, the agent will get back to you')
        send_mail(subject=listing, message=f'{name} has made an inquiry on {listing} with id {listing_id}',
                  from_email='umemytest@gmail.com', recipient_list=[details[0].realtor, 'tony@gmail.com'],
                  fail_silently=False)
        return redirect('listing', listing_id=listing_id)
    return redirect('all_listings')
