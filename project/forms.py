from django import forms
from .models import Profile, Listing, Inquiry

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'address']

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['item_name', 'description', 'price', 'picture', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter a description'}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Enter the price'}),
        }

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your inquiry message here'}),
        }