# define the forms that we use for create/update/delete operss
from django import forms
from .models import Article, Comment

class CreateArticleForm(forms.ModelForm):
    '''A form to add an article to the database'''

    class Meta:
        '''assoc this form with a model from our database'''
        model = Article
        fields = ['author', 'title','text', 'image_url']

class CreateCommentForm(forms.ModelForm):
    '''A form to add a comment abt an article'''

    class Meta:
        '''assoc this form with a model from our database'''
        model = Comment
        fields = ['author', 'text'] 