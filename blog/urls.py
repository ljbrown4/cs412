from django.urls import path
from django.conf import settings
from . import views
from .views import * #ShowAllView, ArticleView, RandomArticleView
 
 
urlpatterns = [
    path('', RandomArticleView.as_view(), name="random"),
    path('show_all', ShowAllView.as_view(), name="show_all"), # modified
    path('article/<int:pk>', ArticleView.as_view(), name='article'),# new module 3
    path('article/create', CreateArticleView.as_view(), name="create_article"), # new module 4
    path('article/<int:pk>/update', UpdateArticleView.as_view(), name="update_article"), # new module 5
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name="create_comment"),
    path('comment/<int:pk>/delete', DeleteCommentView.as_view(), name="delete_comment") # module 5
]