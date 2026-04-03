from django.contrib import admin

# Register your models here.
from .models import Joke, Picture

admin.site.register(Joke)
admin.site.register(Picture)