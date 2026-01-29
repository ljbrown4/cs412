from django.urls import path
from django.conf import settings
from . import views
 
 
urlpatterns = [ 
    path(r'', views.form, name="show_form"),
    path(r'submit', views.submit, name="submit"),
]