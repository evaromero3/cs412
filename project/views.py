from django.shortcuts import render, get_object_or_404, redirect  # Django utilities for rendering templates and handling 404
from django.views.generic import ListView, DetailView, CreateView, View  # Generic views for common patterns
from django.contrib.auth.mixins import LoginRequiredMixin  # Mixin to require authentication for class-based views
from django.contrib.auth.forms import UserCreationForm  # Built-in form for creating users

from .models import Listing, Profile, Category, Inquiry  # Import models for data handling
from django.contrib.auth.models import User  # Django's built-in User model
from .forms import CreateProfileForm, ListingForm, InquiryForm  # Import custom forms for handling user input
from django.contrib import messages  # Utility for displaying success/error messages to users

from django.urls import reverse_lazy  # Lazy evaluation of URL paths
from django.http import HttpResponseRedirect, HttpResponseBadRequest  # Utilities for HTTP responses

# Class-based view for listing all available listings
class ListingListView(ListView):
    model = Listing  # Specify the model to retrieve data from
    template_name = 'project/listing_list.html'  # Template to render
    context_object_name = 'listings'  # Variable name to use in the template

    def get_queryset(self):
        queryset = super().get_queryset()  # Retrieve the default queryset
        category = self.request.GET.get('category')  # Filter by category if provided
        min_price = self.request.GET.get('min_price')  # Minimum price filter
        max_price = self.request.GET.get('max_price')  # Maximum price filter

        queryset = queryset.filter(status='available')  # Only show available listings

        if self.request.user.is_authenticated:
            # Exclude listings from the current user's profile
            current_profile = Profile.objects.filter(user=self.request.user).first()
            queryset = queryset.exclude(seller=current_profile)

        # Apply additional filters
        if category:
            queryset = queryset.filter(category__name=category)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        # Add additional context to the template
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Include all categories for filtering
        return context

# Class-based view for showing listing details
class ListingDetailView(DetailView):
    model = Listing  # Specify the model to retrieve
    template_name = 'project/listing_detail.html'  # Template to render
    context_object_name = 'listing'  # Variable name to use in the template

    def get_context_data(self, **kwargs):
        # Add inquiry form if user is authenticated
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['inquiry_form'] = InquiryForm()
        return context

    def post(self, request, *args, **kwargs):
        # Handle form submission for making an inquiry
        self.object = self.get_object()  # Retrieve the current listing

        if not request.user.is_authenticated:
            # Redirect unauthenticated users to login
            messages.error(request, "You must be logged in to make an inquiry.")
            return redirect('login')

        form = InquiryForm(request.POST)
        if form.is_valid():
            # Save the inquiry and associate it with the listing and current user
            inquiry = form.save(commit=False)
            inquiry.listing = self.object
            inquiry.buyer = Profile.objects.filter(user=self.request.user).first()
            inquiry.save()
            messages.success(request, "Your inquiry has been sent successfully!")
            return HttpResponseRedirect(self.request.path_info)  # Stay on the same page
        return self.get(request, *args, **kwargs)

# Class-based view for managing the user's account
class MyAccountView(LoginRequiredMixin, ListView):
    model = Listing  # Specify the model to retrieve
    template_name = 'project/my_account.html'  # Template to render
    context_object_name = 'listings'  # Variable name to use in the template

    def get_queryset(self):
        # Retrieve listings for the current user's profile
        current_profile = Profile.objects.filter(user=self.request.user).first()
        return Listing.objects.filter(seller=current_profile)

    def get_context_data(self, **kwargs):
        # Add dynamic context based on query parameters
        context = super().get_context_data(**kwargs)
        current_profile = Profile.objects.filter(user=self.request.user).first()

        view = self.request.GET.get('view')  # Determine which view to show
        if view == 'inquiries':
            context['show_inquiries'] = True
            context['inquiries'] = Inquiry.objects.filter(buyer=current_profile)
        elif view == 'received-inquiries':
            context['show_received_inquiries'] = True
            context['received_inquiries'] = Inquiry.objects.filter(
                listing__seller=current_profile
            )
        else:
            context['show_listings'] = True

        context['current_profile'] = current_profile  # Add the profile to context
        context['current_user'] = self.request.user  # Add the user to context
        return context

### USER AUTHENTICATION ###

# Class-based view for creating a new profile
class CreateProfileView(CreateView):
    model = Profile  # Specify the model to create
    template_name = 'project/create_profile.html'  # Template to render
    form_class = CreateProfileForm  # Form class for creating a profile
    success_url = reverse_lazy('my-account')  # Redirect after successful creation

    def get_context_data(self, **kwargs):
        # Add the user creation form to the context
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        # Handle user creation and profile association
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

### CREATING LISTINGS ###

# Class-based view for creating a listing
class CreateListingView(LoginRequiredMixin, CreateView):
    model = Listing  # Specify the model to create
    form_class = ListingForm  # Form class for creating a listing
    template_name = 'project/create_listing.html'  # Template to render
    success_url = reverse_lazy('my-account')  # Redirect after successful creation

    def form_valid(self, form):
        # Automatically assign the seller as the current profile
        current_profile = get_object_or_404(Profile, user=self.request.user)
        form.instance.seller = current_profile
        return super().form_valid(form)

### HANDLE INQUIRY STATUS ###

# Class-based view for accepting or rejecting inquiries
class HandleInquiryView(LoginRequiredMixin, View):
    def post(self, request, inquiry_id, *args, **kwargs):
        action = kwargs.get('action')  # Determine the action from the URL
        inquiry = get_object_or_404(Inquiry, id=inquiry_id)  # Retrieve the inquiry

        if inquiry.listing.seller.user != request.user:
            # Ensure only the seller can manage the inquiry
            messages.error(request, "You are not authorized to manage this inquiry.")
            return redirect('my-account')

        if action == 'accept':
            inquiry.status = 'accepted'
            inquiry.listing.status = 'bought'
            inquiry.listing.save()
            inquiry.save()
            messages.success(request, f"Inquiry for '{inquiry.listing.item_name}' accepted.")
        elif action == 'reject':
            inquiry.status = 'rejected'
            inquiry.save()
            messages.success(request, f"Inquiry for '{inquiry.listing.item_name}' rejected.")
        else:
            return HttpResponseBadRequest("Invalid action.")

        return redirect('my-account')
