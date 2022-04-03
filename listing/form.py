from django import forms

from .models import Listing
from .choices import offer_choices, bedroom_choices, bath_choices, prices_choice, sqft_choice


class ListingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.listing = None
        if 'listing' in kwargs:
            self.listing = kwargs.pop('listing')
        super(ListingForm, self).__init__(*args, **kwargs)
        self.fields['realtor'].initial = self.request.user
        self.fields['realtor'].widget = forms.HiddenInput()
        if self.listing:
            self.fields['title'].initial = self.listing.title
            self.fields['address'].initial = self.listing.address
            self.fields['city'].initial = self.listing.city
            self.fields['state'].initial = self.listing.state
            self.fields['offer_type'].initial = self.listing.offer_type
            self.fields['zipcode'].initial = self.listing.zipcode
            self.fields['price'].initial = self.listing.price
            self.fields['bedrooms'].initial = self.listing.bedrooms
            self.fields['baths'].initial = self.listing.baths
            self.fields['sqft'].initial = self.listing.sqft
            self.fields['garage'].initial = self.listing.garage
            self.fields['pool'].initial = self.listing.pool
            self.fields['description'].initial = self.listing.description
            self.fields['photo_main'].initial = self.listing.photo_main
            self.fields['photo_1'].initial = self.listing.photo_1
            self.fields['photo_2'].initial = self.listing.photo_2
            self.fields['photo_3'].initial = self.listing.photo_3
            self.fields['photo_4'].initial = self.listing.photo_4
            self.fields['photo_5'].initial = self.listing.photo_5
            self.fields['is_published'].initial = self.listing.is_published

    offer_type = forms.ChoiceField(choices=offer_choices)

    class Meta:
        model = Listing
        fields = '__all__'
        exclude = ['list_date']


class SearchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.listings = kwargs.pop('listing')
        self.states = [('', 'State')]
        self.searches = {}
        if 'searches' in kwargs:
            self.searches = kwargs.pop('searches')
        super(SearchForm, self).__init__(*args, **kwargs)
        if self.listings:
            for item in self.listings:
                if item.state not in self.states:
                    self.states.append((item.state, item.state))
            self.states = tuple(sorted(self.states, key=lambda x: x[0]))
            self.fields['state'].widget.choices = self.states
        if 'offer_type' in self.searches:
            self.fields['offer_type'].initial = self.searches['offer_type']
        if 'bedrooms' in self.searches:
            self.fields['bedrooms'].initial = self.searches['bedrooms']
        if 'baths' in self.searches:
            self.fields['baths'].initial = self.searches['baths']
        if 'price' in self.searches:
            self.fields['price'].initial = self.searches['price']
        if 'state' in self.searches:
            self.fields['state'].initial = self.searches['state']
        if 'sqft' in self.searches:
            self.fields['sqft'].initial = self.searches['sqft']

    offer_type = forms.ChoiceField(choices=offer_choices, required=False)
    bedrooms = forms.ChoiceField(choices=bedroom_choices, required=False)
    baths = forms.ChoiceField(choices=bath_choices, required=False)
    price = forms.ChoiceField(choices=prices_choice, required=False)
    state = forms.ChoiceField(choices=bath_choices, required=False)
    sqft = forms.ChoiceField(choices=sqft_choice, required=False)

    class Meta:
        model = Listing
        fields = ['offer_type', 'state', 'bedrooms', 'baths', 'sqft', 'price']
