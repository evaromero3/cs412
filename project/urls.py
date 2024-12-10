from django.urls import path  # Import Django's path function for URL routing
from .views import (
    ListingListView, 
    ListingDetailView, 
    MyAccountView, 
    CreateProfileView, 
    CreateListingView, 
    HandleInquiryView
)  # Import views from your app
from django.contrib.auth.views import LoginView, LogoutView  # Import Django's built-in auth views
from django.contrib.auth import views as auth_views  # Alias for additional auth views

# Define the URL patterns for the application
urlpatterns = [
    # Home page showing the list of listings
    path('', ListingListView.as_view(), name='listing_list'),
    
    # Detail page for a specific listing, identified by primary key (pk)
    path('listings/<int:pk>/', ListingDetailView.as_view(), name='listing_detail'),
    
    # Login page using Django's built-in LoginView with a custom template
    path('login/', LoginView.as_view(template_name='project/login.html'), name='login'),
    
    # My Account page for the logged-in user
    path('my-account/', MyAccountView.as_view(), name='my-account'),
    
    # Logout functionality using Django's built-in LogoutView and redirecting to the listing list
    path('logout/', auth_views.LogoutView.as_view(next_page='listing_list'), name='logout'),
    
    # Page to create a new profile
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    
    # Page to create a new listing
    path('create_listing/', CreateListingView.as_view(), name='create_listing'),
    
    # Endpoint for handling the acceptance of an inquiry
    path(
        'inquiry/<int:inquiry_id>/accept/', 
        HandleInquiryView.as_view(), 
        {'action': 'accept'}, 
        name='accept_inquiry'
    ),
    
    # Endpoint for handling the rejection of an inquiry
    path(
        'inquiry/<int:inquiry_id>/reject/', 
        HandleInquiryView.as_view(), 
        {'action': 'reject'}, 
        name='reject_inquiry'
    ),
]
