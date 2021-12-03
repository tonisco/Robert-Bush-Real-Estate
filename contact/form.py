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
        if self.request.user:
            self.fields['user_id'].initial = self.request.user.id
            self.fields['user_id'].widget.attrs['readonly'] = True

    class Meta:
        model = Contact
        fields = ('listing', 'listing_id', 'name', 'email', 'phone', 'message', 'user_id')
