# File: views.py
# Author: Leigh Brown (ljbrown@bu.edu), 2/12/2026 + 2/19/2026
# Description: create the functions necessary to connect to html templates

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Profile, Post, Photo, Follow
from django.urls import reverse
from django.shortcuts import render
from .forms import * #CreatePostForm, UpdateProfileForm, UpdatePostForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth import login

# Create your views here.

class ProfileRequiredMixin(LoginRequiredMixin):#loginreqmixin sub class
    """Custom mixin that requires auth and returns user profile as need """
   
    def get_profile(self): 
        """ get profile of current user"""
        return Profile.objects.get(user=self.request.user)
    
    def get_login_url(self):
        return reverse('login')

    
    def is_owner(self, profile):
        '''check user is user of current profile being viewed'''
        return self.request.user.is_authenticated and profile.user == self.request.user

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

        profile = self.get_object()


        # add to ctxt data, used to display page specific nav icons
        context['profile'] = profile
        context['is_owner'] = (self.request.user.is_authenticated and profile.user == self.request.user)
        if context['is_owner']:
            context['header_profile_img'] = profile.profile_image_url
            context['create_post_img'] = reverse('create_post')
            context['feed'] = reverse('show_feed')
            context['search_icon'] = reverse('search')

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
        profile = post.profile

        # add to ctxt data, used to display page specific nav icons
        context['back_url'] = reverse('profile', args=[post.profile.pk])
        context['header_profile_img'] = post.profile.profile_image_url

        context['is_owner'] = (
            self.request.user.is_authenticated and profile.user == self.request.user
        )
        if context['is_owner']:
            context['create_post_img'] = reverse('create_post')
            context['feed'] = reverse('show_feed')
            context['search_icon'] = reverse('search')

        return context

class CreatePostView(ProfileRequiredMixin, CreateView):
    '''view to handle post creation'''

    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'
    
    def form_valid(self, form):
        '''this method handles form sub and saved new obj to databse/ we neeed to add for key  to the comm obj b4 saving it to database'''

        # print(form.cleaned_data) #show the form data saved in terminal

        #retrieve profile
        profile = self.get_profile()
        form.instance.profile = profile

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
 
        # retrieve profile
        profile = self.get_profile()

        # add to ctxt data, used to display page specific nav icons
        context['back_url'] = reverse('my_profile')
        context['header_profile_img'] = profile.profile_image_url
        context['back_url'] = reverse('profile', args=[profile.pk])
        context['feed'] = reverse('show_feed')
        context['is_owner'] = True

        return context 
    
class UpdateProfileView(ProfileRequiredMixin, UpdateView):
    ''' view to handle profile updates'''
    model = Profile
    form_class= UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"

    def get_object(self):
        return self.get_profile()

    def get_context_data(self, **kwargs):
        '''return the dict of context variables for use in the template'''
        
        context = super().get_context_data(**kwargs)

        profile = self.get_object()

        # add to ctxt data, used to display page specific nav icons
        context['profile'] = profile
        context['header_profile_img'] = profile.profile_image_url
        context['back_url'] = reverse('my_profile')
        context['is_owner'] = True
        context['feed'] = reverse('show_feed')
        
        return context

    

class DeletePostView(ProfileRequiredMixin, DeleteView):
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
        context['is_owner'] = True
        context['post'] = post
        context['profile'] = profile
        context['header_profile_img'] = profile.profile_image_url
        context['back_url'] = reverse('profile', args=[post.profile.pk])
        context['feed'] = reverse('show_feed')
        

        return context

    def get_success_url(self):
        ''' return to profile page upon successful deletion'''

        #find pk 
        pk = self.kwargs['pk']
        #find comm obj
        post = Post.objects.get(pk=pk)
        profile = post.profile
        return reverse('profile', kwargs={'pk':profile.pk})
    

class UpdatePostView(ProfileRequiredMixin, UpdateView):
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
        context['is_owner'] = True
        context['post'] = post
        context['profile'] = post.profile
        context['header_profile_img'] = post.profile.profile_image_url
        context['back_url'] = reverse('my_profile')
        context['feed'] = reverse('show_feed')

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
        context['is_owner'] = (self.request.user.is_authenticated and profile.user == self.request.user)
        if context['is_owner']:
            context['create_post_img'] = reverse('create_post')
            context['feed'] = reverse('show_feed')
            context['search_icon'] = reverse('search')

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
        context['is_owner'] = (self.request.user.is_authenticated and profile.user == self.request.user)
        if context['is_owner']:
            context['create_post_img'] = reverse('create_post')
            context['feed'] = reverse('show_feed')
            context['search_icon'] = reverse('search')

        return context

class PostFeedListView(ProfileRequiredMixin, ListView):
    ''' show all the posts from the database from users the current profile follows'''
    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        profile = self.get_profile()
        return profile.get_post_feed()
    
    def get_context_data(self, **kwargs):
        '''return the dict of context variables for use in the template'''
        
        context = super().get_context_data(**kwargs)

        profile =self.get_profile()

        # add to ctxt data, used to display page specific nav icons
        context['profile'] = profile
        context['is_owner'] = True
        context['back_url'] = reverse('profile', args=[profile.pk])
        context['header_profile_img'] = profile.profile_image_url
        context['create_post_img'] = reverse('create_post')
        context['feed'] = reverse('show_feed')
        context['search_icon'] = reverse('search')

        return context


class SearchView(ProfileRequiredMixin, ListView):
    ''' allow users to input text to search profiles + captions and then display the results'''
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        self.profile = self.get_profile()

        # check for query in GET
        self.results = self.request.GET.get('results')

        if not self.results:
            context = {}
            context['profile'] = self.profile
            context['header_profile_img'] = self.profile.profile_image_url
            context['back_url'] = reverse('profile', args=[self.profile.pk])
            context['create_post_img'] = reverse('create_post')
            context['feed'] = reverse('show_feed')
            context['search_icon'] = reverse('search')
            return render(request, 'mini_insta/search.html', context)


        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        '''get matching posts to the search'''
        res = self.results
        return Post.objects.filter(caption__icontains=res).order_by('-timestamp')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        
        #nav
        context['profile'] = self.profile
        context['header_profile_img'] = self.profile.profile_image_url
        context['back_url'] = reverse('my_profile')
        context['create_post_img'] = reverse('create_post')
        context['feed'] = reverse('show_feed')
        context['search_icon'] = reverse('search')

        #matching posts
        context['results'] = self.results
        context['posts'] = self.get_queryset()

        #matching profiles
        res = self.results

        context['profiles'] = (
            Profile.objects.filter(username__icontains=res) |
            Profile.objects.filter(display_name__icontains=res) |
            Profile.objects.filter(bio_text__icontains=res)
        ).distinct()




        return context
    

class MyProfileDetailView(ProfileRequiredMixin, DetailView):
    '''get profile of current user'''
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.get_profile()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = context['profile']

        context['header_profile_img'] = profile.profile_image_url
        context['back_url'] = reverse('show_all_profiles')
        context['is_owner'] = True
        context['create_post_img'] = reverse('create_post')
        context['feed'] = reverse('show_feed')
        context['search_icon'] = reverse('search')

        return context
    

class LogOutComfirmationView(TemplateView):
    '''page for users to log out'''
    template_name = "mini_insta/logged_out.html"


class CreateProfileView(CreateView):
    ''' view to handle profile updates'''
    model = Profile
    form_class= CreateProfileForm
    template_name = "mini_insta/create_profile_form.html"

    def form_valid(self, form):

        user = UserCreationForm(self.request.POST)

        if not user.is_valid():
            context = self.get_context_data()
            context['user'] = user
            # so user knows why error occured. googled this
            return self.render_to_response(context)

        
        #create user
        new_user = user.save()
        # log in
        login(self.request, new_user, backend='django.contrib.auth.backends.ModelBackend')

        #attach to profile
        form.instance.user = new_user

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        '''return the dict of context variables for use in the template'''
        
        context = super().get_context_data(**kwargs)

        if 'user' not in context:
            context['user'] = UserCreationForm()

        # add to ctxt data, used to display page specific nav icons
        context['back_url'] = reverse('show_all_profiles')
        context['is_owner'] = False

        return context
    
    def get_success_url(self):
        '''send user to newly created profile upon successful creation'''
        return reverse('my_profile')
