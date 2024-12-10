from django.urls import path
from .views import ListingListView, ListingDetailView, MyAccountView, CreateProfileView, CreateListingView, HandleInquiryView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', ListingListView.as_view(), name='listing_list'),
    path('listings/<int:pk>/', ListingDetailView.as_view(), name='listing_detail'),
    path('login/', LoginView.as_view(template_name='project/login.html'), name='login'),
    path('my-account/', MyAccountView.as_view(), name='my-account'),
    path('logout/', auth_views.LogoutView.as_view(next_page='listing_list'), name='logout'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('create_listing/', CreateListingView.as_view(), name='create_listing'),
    path('inquiry/<int:inquiry_id>/accept/', HandleInquiryView.as_view(), {'action': 'accept'}, name='accept_inquiry'),
    path('inquiry/<int:inquiry_id>/reject/', HandleInquiryView.as_view(), {'action': 'reject'}, name='reject_inquiry'),
]