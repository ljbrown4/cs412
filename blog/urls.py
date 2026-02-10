from django.urls import path
from django.conf import settings
from . import views
from .views import ShowAllView
 
 
urlpatterns = [
    path('', ShowAllView.as_view(), name="show_all")
]