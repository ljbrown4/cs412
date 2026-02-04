from django.urls import path
from django.conf import settings
from . import views

#hw app spec url patters
urlpatterns = [
    #path(r'', views.home, name="home"),
    path(r'', views.main, name="main"),
    path(r'order', views.order, name="order"),
    path(r'submit', views.submit, name="submit"),
]