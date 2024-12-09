from django.db import models

# Create your models here
# Profile Model
class Profile(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Django's built-in User model
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    address = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Listing Model
class Listing(models.Model):
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='listings')
    posted_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    picture = models.ImageField(upload_to='listing_pictures/', blank=True, null=True)
    
    def __str__(self):
        return self.item_name


# Inquiry Model
class Inquiry(models.Model):
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='inquiries')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='inquiries')
    message = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry by {self.buyer.first_name} on {self.listing.item_name}"
