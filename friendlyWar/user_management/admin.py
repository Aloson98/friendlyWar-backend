from django.contrib import admin
from .models import CustomUser, Matches, UserAvatar

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Matches)
admin.site.register(UserAvatar)