from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

from .models import Listing, Profile, Category, Inquiry
from django.contrib.auth.models import User
from .forms import CreateProfileForm, ListingForm, InquiryForm
from django.contrib import messages

from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

# Create your views here.

class ListingListView(ListView):
    model = Listing  # The model to retrieve data from
    template_name = 'project/listing_list.html'  # Template to render the view
    context_object_name = 'listings'  # Name to use for the object list in the template

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        if category:
            queryset = queryset.filter(category__name=category)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Include categories for the filter
        return context


class ListingDetailView(DetailView):
    model = Listing
    template_name = 'project/listing_detail.html'
    context_object_name = 'listing'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inquiry_form'] = InquiryForm()  # Add the inquiry form to the context
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Fetch the current listing
        form = InquiryForm(request.POST)
        if form.is_valid():
            # Save the inquiry and associate it with the listing and current user
            inquiry = form.save(commit=False)
            inquiry.listing = self.object
            inquiry.buyer = Profile.objects.filter(user=self.request.user).first()
            inquiry.save()
            messages.success(request, "Your inquiry has been sent successfully!")
            return HttpResponseRedirect(self.request.path_info)  # Redirect to the same page
        return self.get(request, *args, **kwargs)

class MyAccountView(LoginRequiredMixin, ListView):
    model = Listing
    template_name = 'project/my_account.html'
    context_object_name = 'listings'

    def get_queryset(self):
        # Fetch the current user's profile
        current_profile = Profile.objects.filter(user=self.request.user).first()
        # Fetch listings created by the current profile
        return Listing.objects.filter(seller=current_profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_profile = Profile.objects.filter(user=self.request.user).first()

        # Check the `view` query parameter
        view = self.request.GET.get('view')
        if view == 'inquiries':
            context['show_inquiries'] = True
            context['inquiries'] = Inquiry.objects.filter(buyer=current_profile)
            context['show_listings'] = False
        else:  # Default to showing listings
            context['show_inquiries'] = False
            context['show_listings'] = True

        return context


### USER AUTHENTICATION ### 

class CreateProfileView(CreateView):
    model = Profile
    template_name = 'project/create_profile.html'
    form_class = CreateProfileForm
    success_url = reverse_lazy('my-account')  # Redirect after successful creation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()  # Add UserCreationForm to the context
        return context

    def form_valid(self, form):
        # Handle the UserCreationForm
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            # Save the user
            user = user_form.save()
            # Assign the user to the profile
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return super().form_valid(form)
        else:
            # If the UserCreationForm is invalid, re-render the form with errors
            return self.form_invalid(form)

### Creating Listing ###

class CreateListingView(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = ListingForm
    template_name = 'project/create_listing.html'
    success_url = reverse_lazy('my-account')  # Redirect back to My Account page after successful creation

    def form_valid(self, form):
        # Fetch the current user's profile using the ForeignKey relationship
        current_profile = get_object_or_404(Profile, user=self.request.user)
        # Automatically set the seller as the current profile
        form.instance.seller = current_profile
        return super().form_valid(form)