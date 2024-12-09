from django.contrib import admin
from .models import Profile, Listing, Category, Inquiry

# Register models
admin.site.register(Profile)
admin.site.register(Listing)  # Use the custom ListingAdmin class
admin.site.register(Category)
admin.site.register(Inquiry)
