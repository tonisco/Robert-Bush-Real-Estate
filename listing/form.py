from django import forms

from .models import Listing
from .choices import offer


class ListingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ListingForm, self).__init__(*args, **kwargs)
        # self.fields['realtor'].initial = self.request.user
        self.fields['realtor'].disabled = True

    offer_type = forms.ChoiceField(choices=offer)

    class Meta:
        model = Listing
        fields = '__all__'
