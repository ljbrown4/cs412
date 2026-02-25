from django.db import models
from django.urls import reverse

# Create your models here.
class Article(models.Model):
    '''encapsulate data of blog articles'''
 
    # data attributes
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)
    # image_url = models.URLField(blank=True) #url as a string

    image_file = models.ImageField(blank=True) #an actual image

    def __str__(self): 
        return f'{self.title} by {self.author}'
    
    def get_absolute_url(self):
        '''return a url to display one instance of this mdel
        used to deal with config error when adding articles using form'''
        return reverse('article', kwargs={'pk':self.pk})
    
    def get_all_comments(self):
        '''get all comments on an article'''
        comments = Comment.objects.filter(article=self)
        return comments
    
class Comment(models.Model):
    '''encapsulates idea of a comment abt an article'''

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    #cascade delete, when an article is deleted all comments assoc with it are also deleted
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return string rep of this comment'''
        return f'{self.text}'