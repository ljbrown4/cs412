# File: admin.py
# Author: Leigh Brown (ljbrown@bu.edu), 2/12/2026
# Description: connect class to admin

from django.contrib import admin
from .models import Profile, Photo, Post

# Register your models here.
admin.site.register(Profile)
admin.site.register(Photo)
admin.site.register(Post)