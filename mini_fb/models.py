from django.db import models
from django.urls import reverse

# Profile model for Facebook-like users
class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    email = models.EmailField()
    profile_image_url = models.URLField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # Method to return all status messages for a profile, ordered by timestamp
    def get_status_messages(self):
        return self.statusmessage_set.all().order_by('-timestamp')

    # Optional method to return the absolute URL for a profile (useful for redirecting)
    def get_absolute_url(self):
        return reverse('show_profile', args=[self.pk])


# StatusMessage model to represent Facebook-like status updates
class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Message from {self.profile.first_name} at {self.timestamp}"

    # Add method to get associated images for a StatusMessage
    def get_images(self):
        return self.image_set.all()


# Image model to encapsulate images linked to a StatusMessage
class Image(models.Model):
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)  # Foreign key to StatusMessage
    image_file = models.ImageField(upload_to='images/')  # ImageField to store image files
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp for when the image was uploaded

    def __str__(self):
        return self.image_file.name