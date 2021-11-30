from django import forms

from .models import Listing
from .choices import offer_choices, bedroom_choices, bath_choices, prices_choice, sqft_choice


class ListingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ListingForm, self).__init__(*args, **kwargs)
        # self.fields['realtor'].initial = self.request.user
        self.fields['realtor'].disabled = True

    offer_type = forms.ChoiceField(choices=offer_choices)

    class Meta:
        model = Listing
        fields = '__all__'


class SearchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.listings = kwargs.pop('listing')
        self.states = [('', 'State')]
        super(SearchForm, self).__init__(*args, **kwargs)
        for item in self.listings:
            if item.state not in self.states:
                self.states.append((item.state, item.state))
        self.states = tuple(sorted(self.states, key=lambda x: x[0]))
        self.fields['state'].widget.choices = self.states

    offer_type = forms.ChoiceField(choices=offer_choices, required=False)
    bedrooms = forms.ChoiceField(choices=bedroom_choices, required=False)
    baths = forms.ChoiceField(choices=bath_choices, required=False)
    price = forms.ChoiceField(choices=prices_choice, required=False)
    state = forms.ChoiceField(choices=bath_choices, required=False)
    sqft = forms.ChoiceField(choices=sqft_choice, required=False)

    class Meta:
        model = Listing
        fields = ['offer_type', 'state', 'bedrooms', 'baths', 'sqft', 'price']
