from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Comment
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm
from django.urls import reverse #allows us to create url from an url pattern name
import random

# Create your views here.

class ShowAllView(ListView):
    model = Article
    template_name = 'blog/showall.html'
    context_object_name = 'articles'


class ArticleView(DetailView):
    '''Show the details for one article.'''
    model = Article
    template_name = 'blog/article.html' ## reusing same template!!
    context_object_name = 'article'

class RandomArticleView(DetailView):
    '''Show the details for one article.'''
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'
 
 
    # pick one article at random:
    def get_object(self):
        '''Return one Article object chosen at random.'''
 
 
        all_articles = Article.objects.all()
        return random.choice(all_articles)
 

class CreateArticleView(CreateView):
    '''a view to handle article creation
    1. diplay html form to user (get)
    2. process form sub and sotre new article object (post)'''

    form_class = CreateArticleForm
    template_name = 'blog/create_article_form.html'

    def form_valid(self, form):
        print(f'CreateArticleView.form_valid(): {form.cleaned_data}')
        return super().form_valid(form)

class CreateCommentView(CreateView):
    '''a view to handle comment creation'''

    form_class = CreateCommentForm
    template_name = 'blog/create_comment_form.html'

    def get_success_url(self):
        '''return url to redirect after succ sub form. for config error'''
        # return reverse('show_all')

        pk = self.kwargs['pk']
        return reverse('article', kwargs={'pk':pk})
    
    def form_valid(self, form):
        '''this method handles form sub and saved new obj to databse/ we neeed to add for key  to the comm obj b4 saving it to database'''

        print(form.cleaned_data) #show the form data saved in terminal

        #retrieve pk from url pattern
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
        #attach art to comm
        form.instance.article = article #set the fk

        #delegate to superclass meth
        return super().form_valid(form)
    
    def get_context_data(self):
        '''return the dict of context variables for use in the template'''

        #call super
        context = super().get_context_data()
 
        #retrieve pk from url pattern
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)

        #add to ctxt data
        context['article'] = article
        return context 
    

class UpdateArticleView(UpdateView):
    model = Article
    form_class= UpdateArticleForm
    template_name = "blog/update_article_form.html"

class DeleteCommentView(DeleteView):
    model = Comment
    template_name = "blog/delete_comment_form.html"

    def get_success_url(self):
        #find pk 
        pk = self.kwargs['pk']
        #find comm obj
        comment = Comment.objects.get(pk=pk)
        article = comment.article
        return reverse('article', kwargs={'pk':article.pk})
    