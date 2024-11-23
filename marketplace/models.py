from django.db import models

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Listing(models.Model):
    item_name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    posted_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.item_name

class Inquiry(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer_inquiries")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    message = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry from {self.buyer} about {self.listing}"