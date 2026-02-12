from django.urls import path
from django.conf import settings
from . import views
from .views import ShowAllView, ArticleView, RandomArticleView
 
 
urlpatterns = [
    path('', RandomArticleView.as_view(), name="random"),
    path('show_all', ShowAllView.as_view(), name="show_all"), # modified
    path('article/<int:pk>', ArticleView.as_view(), name='article'),# new
]