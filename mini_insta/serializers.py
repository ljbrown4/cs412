# File: serializers.py
# Author: Leigh Brown (ljbrown4@bu.edu), 4/07/2026
# Description: convert django models into text to send over HTTP

from rest_framework import serializers
from .models import *

class ProfileSerializer(serializers.ModelSerializer):
    '''serializer for the joke model. specificies which fields are sent to the API'''
    #posts = serializers.SerializerMethodField()
    num_posts = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    num_followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    num_following = serializers.SerializerMethodField()
    pk = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['username', 'user', 'display_name', 'bio_text', 'join_date', 'profile_image_url', 'num_posts', 'followers', 
                  'num_followers','following','num_following', 'pk']

    #customize create operation
    def create(self, validated_data):
        '''override create superclass method'''
        print(f'ProfileSerializer.create, validated_data={validated_data}.')

        return Profile.objects.create(**validated_data)
    
    
    # def get_posts(self, obj):
    #     #get the photo from each post and the pk so that u can display the photo and use it to go to the corresponding profile page
    #     posts = Post.objects.filter(profile=obj).order_by('-timestamp')
    #     return []
    
    def get_num_posts(self, obj):
        posts = Post.objects.filter(profile=obj).order_by('-timestamp')
        return len(posts)
    
    def get_followers(self, obj):
        followers = list(Follow.objects.filter(profile=obj))
        return [f.follower_profile.pk for f in followers]
    
    def get_num_followers(self, obj):
        followers = list(Follow.objects.filter(profile=obj))
        return len(followers)
    
    def get_following(self, obj):
        following = list(Follow.objects.filter(follower_profile=obj))
        return [f.pk for f in following]
    
    def get_num_following(self, obj):
        following = list(Follow.objects.filter(follower_profile=obj))
        return len(following)
    
    def get_pk(self, obj):
        return obj.pk

    
class PostSerializer(serializers.ModelSerializer):
    '''serializer for the joke model. specificies which fields are sent to the API'''
    first_photo = serializers.SerializerMethodField() #asked how to add class level methods from models.py to serializers
    username = serializers.SerializerMethodField()
    display_name = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    two_comments = serializers.SerializerMethodField()
    all_photos = serializers.SerializerMethodField()
    first_like = serializers.SerializerMethodField()
    num_likes = serializers.SerializerMethodField()
    pfp = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['profile', 'caption', 'timestamp', 'first_photo', 'username', 'display_name', 'comments', 'first_like', 'all_photos', 'num_likes', 'two_comments', 'pk', 'pfp']

    #customize create operation
    def create(self, validated_data):
        '''override create superclass method'''
        print(f'PostSerializer.create, validated_data={validated_data}.')

        return Post.objects.create(**validated_data)
    
    #class methods 
    def get_all_photos(self, obj):
        '''get all photos for a post'''
        photos = Photo.objects.filter(post=obj)

        return [p.image_url if p.image_url else p.image_file.url for p in photos]
        
    def get_username(self, obj):
        return obj.profile.username
    
    def get_two_comments(self, obj): #show less comments on the main page for space saving
        #get the username of the commenter and the comment itself
        comments = Comment.objects.filter(post=obj)[:2]
        return [c.profile.username + " " + c.text for c in comments]
    
    def get_comments(self, obj):
        #get the username of the commenter and the comment itseld
        comments = Comment.objects.filter(post=obj)
        return [c.profile.username + " " + c.text for c in comments]

    def get_pfp(self, obj):
        return obj.profile.profile_image_url
    
    def get_display_name(self, obj):
        return obj.profile.display_name

    def get_first_photo(self, obj):
        photo = obj.get_first_photo()

        if photo:
            if photo.image_file:
                return photo.image_file.url #so i can put into image tag and use uri
            elif photo.image_url:
                return photo.image_url

        return None
    
    def get_pk(self, obj):
        return obj.pk
    
    def get_num_likes(self, obj):
        likes = Like.objects.filter(post=obj)
        num = len(likes)
        if num > 1:
            return num - 1 #1st alr displayed
        else:
            return 0
    
    def get_first_like(self, obj):
        like = Like.objects.filter(post=obj).first()
        if like and like.profile:
            return like.profile.username
        return ""  # no likes case
    
class PhotoSerializer(serializers.ModelSerializer):
    '''serializer for the joke model. specificies which fields are sent to the API'''

    class Meta:
        model = Photo
        fields = ['post', 'image_file', 'timestamp', 'image_url']

    #customize create operation
    def create(self, validated_data):
        '''override create superclass method'''
        print(f'PhotoSerializer.create, validated_data={validated_data}.')

        return Photo.objects.create(**validated_data)

    
class CommentSerializer(serializers.ModelSerializer):
    '''serializer for the joke model. specificies which fields are sent to the API'''

    class Meta:
        model = Comment
        fields = ['profile', 'post', 'timestamp', 'text']

    #customize create operation
    def create(self, validated_data):
        '''override create superclass method'''
        print(f'CommentSerializer.create, validated_data={validated_data}.')

        return Comment.objects.create(**validated_data)
    
class FollowSerializer(serializers.ModelSerializer):
    '''serializer for the joke model. specificies which fields are sent to the API'''

    class Meta:
        model = Follow
        fields = ['profile', 'follower_profile', 'timestamp']

    #customize create operation
    def create(self, validated_data):
        '''override create superclass method'''
        print(f'FollowSerializer.create, validated_data={validated_data}.')

        return Follow.objects.create(**validated_data)
    
class LikeSerializer(serializers.ModelSerializer):
    '''serializer for the joke model. specificies which fields are sent to the API'''

    class Meta:
        model = Like
        fields = ['profile', 'post', 'timestamp']

    #customize create operation
    def create(self, validated_data):
        '''override create superclass method'''
        print(f'LikeSerializer.create, validated_data={validated_data}.')

        return Like.objects.create(**validated_data)


