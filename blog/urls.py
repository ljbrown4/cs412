from django.urls import path
from django.conf import settings
from . import views
from .views import * #ShowAllView, ArticleView, RandomArticleView
from django.contrib.auth import views as auth_views
 
urlpatterns = [
    path('', RandomArticleView.as_view(), name="random"),
    path('show_all', ShowAllView.as_view(), name="show_all"), # modified
    path('article/<int:pk>', ArticleView.as_view(), name='article'),# new module 3
    path('article/create', CreateArticleView.as_view(), name="create_article"), # new module 4
    path('article/<int:pk>/update', UpdateArticleView.as_view(), name="update_article"), # new module 5
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name="create_comment"),
    path('comment/<int:pk>/delete', DeleteCommentView.as_view(), name="delete_comment"), # module 5
    path('login/', auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"), #module 6
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all'), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='register'),

    # API views: module 9
    path(r'api/articles/', ArticleListAPIView.as_view()),
    path(r'api/article/<int:pk>', ArticleDetailAPIView.as_view()),
]
