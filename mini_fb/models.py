from django.db import models
from django.urls import reverse
from django.utils import timezone

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

     # New: Method to retrieve all friends for the Profile
    def get_friends(self):
        friends = Friend.objects.filter(models.Q(profile1=self) | models.Q(profile2=self))
        friend_profiles = []
        for friend in friends:
            if friend.profile1 == self:
                friend_profiles.append(friend.profile2)
            else:
                friend_profiles.append(friend.profile1)
        return friend_profiles
    
    def add_friend(self, other):
        if self != other:  # Avoid self-friending
            existing_friend = Friend.objects.filter(
                models.Q(profile1=self, profile2=other) | models.Q(profile1=other, profile2=self)
            )
            if not existing_friend.exists():
                Friend.objects.create(profile1=self, profile2=other, timestamp=timezone.now())


    def get_friend_suggestions(self):
        # Get all current friends' IDs
        friend_ids = [f.profile1.id if f.profile2 == self else f.profile2.id for f in Friend.objects.filter(profile1=self) | Friend.objects.filter(profile2=self)]

        # Add the current profile's ID to exclude self from suggestions
        friend_ids.append(self.id)

        # Filter profiles that are not in the friend list and not self
        suggestions = Profile.objects.exclude(id__in=friend_ids)
        return suggestions

    def get_news_feed(self):
        friend_profiles = self.get_friends()
        all_profiles = [self] + friend_profiles  # Include self and friends
        return StatusMessage.objects.filter(profile__in=all_profiles).order_by('-timestamp')

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

# Friend model to represent friendships between profiles
class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile1} & {self.profile2}"