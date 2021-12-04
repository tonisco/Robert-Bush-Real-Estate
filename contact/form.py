from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.listing = kwargs.pop('listing')
        self.request = kwargs.pop('request')
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['listing_id'].initial = self.listing.id
        self.fields['listing_id'].widget.attrs['readonly'] = True
        self.fields['listing'].widget.attrs['readonly'] = True
        self.fields['listing'].initial = self.listing.title
        self.fields['realtor'].widget = forms.HiddenInput()
        self.fields['realtor'].initial = self.listing.realtor.email
        if self.request.user.is_authenticated:
            self.fields['name'].initial = self.request.user.last_name + ' ' + self.request.user.first_name
            self.fields['email'].initial = self.request.user.email
            self.fields['user_id'].initial = self.request.user.id
            self.fields['user_id'].widget.attrs['readonly'] = True

    class Meta:
        model = Contact
        fields = ('realtor', 'listing', 'listing_id', 'name', 'email', 'phone', 'message', 'user_id')
