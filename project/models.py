from django.db import models  # Import Django's ORM for defining models

# Profile Model: Represents user profiles in the system
class Profile(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Connect to Django's built-in User model
    first_name = models.CharField(max_length=50)  # First name of the user
    last_name = models.CharField(max_length=50)  # Last name of the user
    email = models.EmailField(unique=True)  # Unique email address
    address = models.TextField()  # Address of the user

    def __str__(self):
        return f"{self.first_name} {self.last_name}"  # String representation of the Profile

# Category Model: Represents categories under which listings are organized
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Name of the category
    description = models.TextField(blank=True, null=True)  # Optional description of the category

    def __str__(self):
        return self.name  # String representation of the Category

# Listing Model: Represents an item that a user wants to sell
class Listing(models.Model):
    item_name = models.CharField(max_length=100)  # Name of the item
    description = models.TextField()  # Description of the item
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the item
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='listings')  # Seller of the item (Profile)
    posted_date = models.DateTimeField(auto_now_add=True)  # Date when the listing was created
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )  # Optional category of the item
    picture = models.ImageField(upload_to='listing_pictures/', blank=True, null=True)  # Optional picture of the item

    status = models.CharField(
        max_length=10,
        choices=[('available', 'Available'), ('bought', 'Bought')],  # Choices for listing status
        default='available'  # Default status is 'available'
    )
    
    def __str__(self):
        return self.item_name  # String representation of the Listing

# Inquiry Model: Represents inquiries made by buyers for a listing
class Inquiry(models.Model):
    buyer = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='inquiries'
    )  # The Profile of the buyer making the inquiry
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name='inquiries'
    )  # The listing the inquiry is about
    message = models.TextField()  # The message in the inquiry
    sent_date = models.DateTimeField(auto_now_add=True)  # Date and time when the inquiry was sent

    status = models.CharField(
        max_length=10,
        choices=[
            ('pending', 'Pending'), 
            ('accepted', 'Accepted'), 
            ('rejected', 'Rejected')
        ],  # Choices for inquiry status
        default='pending'  # Default status is 'pending'
    )

    def __str__(self):
        return f"Inquiry by {self.buyer.first_name} on {self.listing.item_name}"  # String representation of the Inquiry
