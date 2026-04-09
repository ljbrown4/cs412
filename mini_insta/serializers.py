# File: serializers.py
# Author: Leigh Brown (ljbrown@bu.edu), 4/07/2026
# Description: convert django models into text to send over HTTP

from rest_framework import serializers
from .models import *

class ProfileSerializer(serializers.ModelSerializer):
    '''serializer for the joke model. specificies which fields are sent to the API'''
    #all_posts = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['username', 'user', 'display_name', 'bio_text', 'join_date', 'profile_image_url']

    #customize create operation
    def create(self, validated_data):
        '''override create superclass method'''
        print(f'ProfileSerializer.create, validated_data={validated_data}.')

        return Profile.objects.create(**validated_data)
    
    
    # def get_all_posts(self, obj):
    #     return obj.get_all_posts()
    
class PostSerializer(serializers.ModelSerializer):
    '''serializer for the joke model. specificies which fields are sent to the API'''
    first_photo = serializers.SerializerMethodField() #asked how to add class level methods from models.py to serializers
    username = serializers.SerializerMethodField()
    display_name = serializers.SerializerMethodField()
    #all_photos = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['profile', 'caption', 'timestamp', 'first_photo', 'username', 'display_name']

    #customize create operation
    def create(self, validated_data):
        '''override create superclass method'''
        print(f'PostSerializer.create, validated_data={validated_data}.')

        return Post.objects.create(**validated_data)
    
    #class methods 
    # def get_all_photos(self, obj):
    #     '''get all photos for a post'''
    #     return obj.get_all_photos()

    def get_username(self, obj):
        return obj.profile.username
    
    def get_displayname(self, obj):
        return obj.profile.display_name

    def get_first_photo(self, obj):
        photo = obj.get_first_photo()

        if photo:
            if photo.image_file:
                return photo.image_file.url #so i can put into image tag and use uri
            elif photo.image_url:
                return photo.image_url

        return None
    
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


