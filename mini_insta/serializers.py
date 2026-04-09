# File: serializers.py
# Author: Leigh Brown (ljbrown@bu.edu), 4/07/2026
# Description: convert django models into text to send over HTTP

from rest_framework import serializers
from .models import *

class ProfileSerializer(serializers.ModelSerializer):
    '''serializer for the joke model. specificies which fields are sent to the API'''
    post_feed = serializers.SerializerMethodField()
    all_posts = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['username', 'user', 'display_name', 'bio_text', 'join_date', 'profile_image_url']

    #customize create operation
    def create(self, validated_data):
        '''override create superclass method'''
        print(f'ProfileSerializer.create, validated_data={validated_data}.')

        return Profile.objects.create(**validated_data)
    
    #class level methods from models.py 
    def get_post_feed(self, obj):
        return obj.get_post_feed()
    
    def get_all_posts(self, obj):
        return obj.get_all_posts()
    
class PostSerializer(serializers.ModelSerializer):
    '''serializer for the joke model. specificies which fields are sent to the API'''
    first_photo = serializers.SerializerMethodField()
    all_photos = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['profile', 'caption', 'timestamp']

    #customize create operation
    def create(self, validated_data):
        '''override create superclass method'''
        print(f'PostSerializer.create, validated_data={validated_data}.')

        return Post.objects.create(**validated_data)
    
    #class methods 
    def get_all_photos(self, obj):
        '''get all photos for a post'''
        return obj.get_all_photos()

    def get_first_photo(self, obj):
        photo = obj.get_first_photo()

        if photo:
            return photo.image_file.url #so i can put into image tag and use uri

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


