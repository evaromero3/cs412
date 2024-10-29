from django.contrib import admin
from .models import Profile
from .models import StatusMessage
from .models import Image
from .models import Friend

# Register your models here.
admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(Friend)  # Register the Friend model