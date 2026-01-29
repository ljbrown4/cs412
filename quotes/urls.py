from django.urls import path
from django.conf import settings
from . import views

#hw app spec url patters
urlpatterns = [
    path(r'', views.home_page, name="home_page"),
    path(r'quotes', views.home_page, name="home_page"),
    path(r'about', views.about, name="about_page"),
    path(r'showall', views.showall, name="showall_page"),
]