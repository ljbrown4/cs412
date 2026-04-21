# File: views.py
# Author: Leigh Brown (ljbrown4@bu.edu), 2/12/2026 + 2/19/2026
# Description: create the functions necessary to connect to html templates

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Profile, Post, Photo, Follow, Like
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import * #CreatePostForm, UpdateProfileForm, UpdatePostForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse 

# Create your views here.
#api imports
from rest_framework import generics
from .serializers import *

#login api imports
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication



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

        #for like and follow
        if self.request.user.is_authenticated:
            current = Profile.objects.get(user=self.request.user)
            context['current'] = current
            context['follows'] = current.is_following(profile)

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

        #for like and follow
        if self.request.user.is_authenticated:
            current = Profile.objects.get(user=self.request.user)
            context['current'] = current
            context['liked'] = post.is_liked_by(current)

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
            Profile.objects.filter(bio_text__icontains=res)).distinct()

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
    

class CreateFollowView(ProfileRequiredMixin, TemplateView):
    '''allow logged in user to follow another profile'''

    def dispatch(self, request, *args, **kwargs):
        current = self.get_profile()
        other = Profile.objects.get(pk=self.kwargs['pk'])

        # profile can't follow itself
        if current != other:
            exists = Follow.objects.filter(profile=other, follower_profile=current).exists()

            if not exists:
                Follow.objects.create(
                    profile=other,
                    follower_profile=current)

        return redirect('profile', pk=other.pk) #reverse wouldn't work here for some reason, looked this up
    
class DeleteFollowView(ProfileRequiredMixin, TemplateView):
    '''allow logged in user to unfollow another profile'''

    def dispatch(self, request, *args, **kwargs):
        current = self.get_profile()
        other = Profile.objects.get(pk=self.kwargs['pk'])

        Follow.objects.filter(
            profile=other,
            follower_profile=current).delete()

        return redirect('profile', pk=other.pk)
    
class CreateLikeView(ProfileRequiredMixin, TemplateView):
    '''allow logged in user to follow another profile'''

    def dispatch(self, request, *args, **kwargs):
        current = self.get_profile()
        post = Post.objects.get(pk=self.kwargs['pk'])

        # profile can't follow itself
        if post.profile != current:
            exists = Like.objects.filter(post=post, profile=current).exists()

            if not exists:
                Like.objects.create(
                    post=post,
                    profile=current)

        return redirect('post', pk=post.pk)
    
class DeleteLikeView(ProfileRequiredMixin, TemplateView):
    '''allow logged in user to unfollow another profile'''

    def dispatch(self, request, *args, **kwargs):
        current = self.get_profile()
        post = Post.objects.get(pk=self.kwargs['pk'])

        Like.objects.filter(
            post=post,
            profile=current).delete()

        return redirect('post', pk=post.pk)


class CreateCommentView(ProfileRequiredMixin, CreateView):
    '''view to handle comment creation'''

    form_class = CreateCommentForm
    template_name = 'mini_insta/create_comment_form.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('post', kwargs={'pk': pk})

    def form_valid(self, form):
        post = Post.objects.get(pk=self.kwargs['pk'])
        profile = self.get_profile()

        form.instance.post = post
        form.instance.profile = profile

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = Post.objects.get(pk=self.kwargs['pk'])
        profile = self.get_profile()

        context['post'] = post
        context['profile'] = profile
        context['header_profile_img'] = profile.profile_image_url
        context['back_url'] = reverse('post', args=[post.pk])
        context['create_post_img'] = reverse('create_post')
        context['feed'] = reverse('show_feed')
        context['search_icon'] = reverse('search')
        context['is_owner'] = True

        return context
    
    
class DeleteCommentView(ProfileRequiredMixin, DeleteView):
    '''view to handle comment deletion. this is allowed by profile who made the post and profile who wrote the comment'''

    model = Comment
    template_name = 'mini_insta/delete_comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        current = self.get_profile()

        # allow deletion if current user wrote comment OR owns the post
        if comment.profile != current and comment.post.profile != current:
            return HttpResponse("You cannot delete this comment.")

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        comment = self.get_object()
        return reverse('post', kwargs={'pk': comment.post.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comment = self.get_object()
        profile = self.get_profile()

        context['comment'] = comment
        context['post'] = comment.post
        context['profile'] = profile
        context['header_profile_img'] = profile.profile_image_url
        context['back_url'] = reverse('post', args=[comment.post.pk])
        context['create_post_img'] = reverse('create_post')
        context['feed'] = reverse('show_feed')
        context['search_icon'] = reverse('search')
        context['is_owner'] = True

        return context
    

#api views
#profile views
class ProfileListAPIView(generics.ListCreateAPIView):
  '''An API view to return a listing of Profiles and to create an Profile.'''
  queryset = Profile.objects.all().order_by('-join_date')
  serializer_class = ProfileSerializer

class ProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''An API view to return a single Profile.'''
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

#post views
class PostFeedAPIView(generics.ListCreateAPIView):
  '''An API view I plan to use to create a new post and display feed.
  1. when user is logged in and follows people feed is trunchated to only show posts from users they follow
  2. when user is not logged in or does not follow anyone feed is all posts within the app'''

  serializer_class = PostSerializer
  #
  authentication_classes = [TokenAuthentication]
  
  def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []
  
  def get_queryset(self): #get user if authenticated and call get post feed for that user
        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)
            following = Follow.objects.filter(follower_profile=profile)
            #only use get_post_feed if user follows ppl otherwise the feed would be empty
            if following.exists(): 
                return profile.get_post_feed()

            return Post.objects.all().order_by('-timestamp') #logged in but follows no one

        return Post.objects.all().order_by('-timestamp') #guest user j sees all posts in the app
  
  def perform_create(self, serializer): #this is to try and make sure that the images are added when a post is created
    profile = Profile.objects.get(user=self.request.user)
    post = serializer.save(profile=profile)

    for image in self.request.FILES.getlist('image_file'): #create a instance of the photo object for each picture uploaded
        Photo.objects.create(
            post=post,
            image_file=image
    )

class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
  '''An API view to return a post.'''
  queryset = Post.objects.all()
  serializer_class = PostSerializer

#for a singular profile
class ProfilePostListAPIView(generics.ListAPIView):
  '''An API view to return all posts associated with a profile'''
  serializer_class = PostSerializer

  def get_queryset(self):
        pk = self.kwargs['pk']
        return Post.objects.filter(profile__pk=pk).order_by('-timestamp')
  
class MyProfilePostListAPIView(generics.ListAPIView):
    '''An API view to return list of all posts of the currently logged in user'''
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        return Post.objects.filter(profile=profile).order_by('-timestamp')
  
#current user's profile
class MyProfileAPIView(generics.RetrieveAPIView):
    '''An API view to return profile of currently logged in user'''
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


#follower + following views
class FollowerListAPIView(generics.ListAPIView):
  '''An API view to return a list of followers for a profile. for Profile'''
  serializer_class = ProfileSerializer

  def get_queryset(self):
        pk = self.kwargs['pk']
        return Profile.objects.filter(follower_profile__profile__pk=pk)
  
class MyFollowerListAPIView(generics.ListAPIView): #update
    '''An API view to return list of followers for currently logged in user. for MyProfile'''
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        return Profile.objects.filter(follower_profile__profile=profile).distinct()
 
class FollowingListAPIView(generics.ListAPIView):
  '''An API view to return a list of people a profile follows.'''
  serializer_class = ProfileSerializer

  def get_queryset(self):
        pk = self.kwargs['pk']
        return Profile.objects.filter(profile__follower_profile__pk=pk)
  
class MyFollowingListAPIView(generics.ListAPIView): #update
    '''An API view to return list of followed profiles for currently logged in user. for MyProfile'''
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        return Profile.objects.filter(profile__follower_profile=profile).distinct()
  
#comment views
class CommentListAPIView(generics.ListCreateAPIView):
  '''An API view I plan to return all comments associated with a specific post'''
  
  serializer_class = CommentSerializer
  def get_queryset(self):
    pk = self.kwargs['pk']
    return Comment.objects.filter(post__pk=pk).order_by('timestamp')
  
  def perform_create(self, serializer):
    profile = Profile.objects.get(user=self.request.user)
    post = Post.objects.get(pk=self.kwargs['pk'])
    serializer.save(profile=profile, post=post)


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
  '''An API view to allow comment creation and deletion.'''
  queryset = Comment.objects.all()
  serializer_class = CommentSerializer

#like views
class LikeListAPIView(generics.ListCreateAPIView):
  '''An API view to return all likes associated with a specific post '''
  serializer_class = LikeSerializer
  authentication_classes = [TokenAuthentication]
  
  def get_permissions(self):
    if self.request.method == 'POST':
        return [IsAuthenticated()]
    return []
  
  def get_queryset(self):
    return Like.objects.all().order_by('-timestamp')
  
  def perform_create(self, serializer):
    profile = Profile.objects.get(user=self.request.user)
    post_pk = self.request.data.get('post')
    post = Post.objects.get(pk=post_pk)

    exists = Like.objects.filter(profile=profile, post=post).exists()

    if not exists:
        serializer.save(profile=profile, post=post)

class LikeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
  '''An API view to allow like creation and deletion.'''
  queryset = Like.objects.all()
  serializer_class = LikeSerializer

#login view
class LoginAPIView(APIView):
    '''An API View for user authentication and login'''
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):

        user = authenticate(request, username=request.data.get('username'), password=request.data.get('password'))

        print(f'LoginAPIView.post(): user ={user}')

        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)

            return Response({ 'token': token.key, 'username': user.username,}, status=status.HTTP_200_OK)

        return Response({'error': 'invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
