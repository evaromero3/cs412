from django import forms  # Import Django's forms module
from .models import Profile, Listing, Inquiry  # Import models for creating forms

# Form for creating a user profile
class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile  # Specify the model to use
        fields = ['first_name', 'last_name', 'email', 'address']  # Fields to include in the form

# Form for creating or editing a listing
class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing  # Specify the model to use
        fields = ['item_name', 'description', 'price', 'picture', 'category']  # Fields to include in the form
        widgets = {
            # Custom widget for the description field
            'description': forms.Textarea(attrs={
                'rows': 4,  # Set the number of rows for the textarea
                'placeholder': 'Enter a description'  # Placeholder text
            }),
            # Custom widget for the price field
            'price': forms.NumberInput(attrs={
                'step': '0.01',  # Step size for decimal input
                'placeholder': 'Enter the price'  # Placeholder text
            }),
        }

# Form for creating an inquiry
class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry  # Specify the model to use
        fields = ['message']  # Field to include in the form
        widgets = {
            # Custom widget for the message field
            'message': forms.Textarea(attrs={
                'placeholder': 'Enter your inquiry message here'  # Placeholder text
            }),
        }
        labels = {
            'message': '',  # Remove the label for the message field
        }
