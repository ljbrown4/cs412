# File: views.py
# Author: Leigh Brown (ljbrown@bu.edu), 2/12/2026 + 2/19/2026
# Description: create the functions necessary to connect to html templates

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Post, Photo, Follow
from django.urls import reverse
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm

# Create your views here.

class ProfileListView(ListView):
    ''' show all the profiles stored in the database'''
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'


class ProfileDetailView(DetailView):
    '''Show the information for one profle.'''
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        '''return the dict of context variables for use in the template'''
        
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # add to ctxt data, used to display page specific nav icons
        context['profile'] = profile
        context['header_profile_img'] = profile.profile_image_url
        context['create_post_img'] = reverse('create_post', args=[pk])
        context['feed'] = reverse('show_feed', args=[pk])

        return context

class PostFeedListView(ListView):
    ''' show all the posts from the database from users the current profile follows'''
    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        profile = Profile.objects.get(pk=pk)
        return profile.get_post_feed()
    
    def get_context_data(self, **kwargs):
        '''return the dict of context variables for use in the template'''
        
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # add to ctxt data, used to display page specific nav icons
        context['profile'] = profile
        context['back_url'] = reverse('profile', args=[profile.pk])
        context['header_profile_img'] = profile.profile_image_url
        context['create_post_img'] = reverse('create_post', args=[pk])
        context['feed'] = reverse('show_feed', args=[pk])

        return context

class PostDetailView(DetailView):
    '''Show the information for one post.'''
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        '''return the dict of context variables for use in the template'''

        # call super
        context = super().get_context_data(**kwargs)

        # retrieve pk from url pattern
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)

        # add to ctxt data, used to display page specific nav icons
        context['back_url'] = reverse('profile', args=[post.profile.pk])
        context['header_profile_img'] = post.profile.profile_image_url
        context['feed'] = reverse('show_feed', args=[post.profile.pk])

        return context

class CreatePostView(CreateView):
    '''view to handle post creation'''

    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'
    
    def form_valid(self, form):
        '''this method handles form sub and saved new obj to databse/ we neeed to add for key  to the comm obj b4 saving it to database'''

        print(form.cleaned_data) #show the form data saved in terminal

        #retrieve pk from url pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        #attach profile to post
        form.instance.profile = profile #set the fk
        response = super().form_valid(form)

        #access image url from photos model
        for image in self.request.FILES.getlist('image_file'):
            Photo.objects.create(
                post=self.object,
                image_file=image
            )

        #delegate to superclass method
        return response
    
    def get_context_data(self):
        '''return the dict of context variables for use in the template'''

        #call super
        context = super().get_context_data()
 
        # retrieve pk from url pattern
        pk = self.kwargs['pk']
       
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile

        # add to ctxt data, used to display page specific nav icons
        context['back_url'] = reverse('profile', args=[pk])
        context['header_profile_img'] = profile.profile_image_url
        context['back_url'] = reverse('profile', args=[profile.pk])
        context['feed'] = reverse('show_feed', args=[profile.pk])

        return context 
    
class UpdateProfileView(UpdateView):
    ''' view to handle profile updates'''
    model = Profile
    form_class= UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"

    def get_context_data(self, **kwargs):
        '''return the dict of context variables for use in the template'''
        
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # add to ctxt data, used to display page specific nav icons
        context['profile'] = profile
        context['header_profile_img'] = profile.profile_image_url
        context['back_url'] = reverse('profile', args=[profile.pk])
        context['feed'] = reverse('show_feed', args=[profile.pk])

        return context

    

class DeletePostView(DeleteView):
    ''' view to handle post deletion '''
    model = Post
    template_name = "mini_insta/delete_post_form.html"

    def get_context_data(self, **kwargs):
        #call super
        context = super().get_context_data(**kwargs)

        #get pk
        pk = self.kwargs['pk']

        #find comm obj
        post = Post.objects.get(pk=pk)
        profile = post.profile

        #add to context data
        context['post'] = post
        context['profile'] = profile
        context['header_profile_img'] = profile.profile_image_url
        context['back_url'] = reverse('profile', args=[post.profile.pk])
        context['feed'] = reverse('show_feed', args=[post.profile.pk])
        

        return context

    def get_success_url(self):
        ''' return to profile page upon successful deletion'''

        #find pk 
        pk = self.kwargs['pk']
        #find comm obj
        post = Post.objects.get(pk=pk)
        profile = post.profile
        return reverse('profile', kwargs={'pk':profile.pk})
    

class UpdatePostView(UpdateView):
    ''' view to handle post updates '''
    model = Post
    form_class= UpdatePostForm
    template_name = "mini_insta/update_post_form.html"

    def get_context_data(self, **kwargs):
        #call super
        context = super().get_context_data(**kwargs)

        #get pk
        pk = self.kwargs['pk']

        #find comm obj
        post = Post.objects.get(pk=pk)

        #add to context data
        context['post'] = post
        context['profile'] = post.profile
        context['header_profile_img'] = post.profile.profile_image_url
        context['back_url'] = reverse('profile', args=[post.profile.pk])
        context['feed'] = reverse('show_feed', args=[post.profile.pk])

        return context

    def get_success_url(self):
        ''' return to profile page upon successful deletion '''

        #find pk 
        pk = self.kwargs['pk']
        #find comm obj
        post = Post.objects.get(pk=pk)
        return reverse('post', kwargs={'pk':post.pk})
    
class ShowFollowersDetailView(DetailView):
    ''' view to show all followers '''

    model = Follow
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        '''return the dict of context variables for use in the template '''
        
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # add to ctxt data, used to display page specific nav icons
        context['profile'] = profile
        context['header_profile_img'] = profile.profile_image_url
        context['back_url'] = reverse('profile', args=[profile.pk])
        context['feed'] = reverse('show_feed', args=[profile.pk])

        return context


class ShowFollowingDetailView(DetailView):
    ''' view to show all following '''

    model = Follow
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        '''return the dict of context variables for use in the template'''
        
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # add to ctxt data, used to display page specific nav icons
        context['profile'] = profile
        context['header_profile_img'] = profile.profile_image_url
        context['back_url'] = reverse('profile', args=[profile.pk])
        context['feed'] = reverse('show_feed', args=[profile.pk])
        return context
    