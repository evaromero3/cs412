from django.contrib import admin
from .models import Profile
from .models import StatusMessage
from .models import Image

# Register your models here.
admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)