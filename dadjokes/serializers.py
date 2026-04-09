# File: serializers.py
# Author: Leigh Brown (ljbrown4@bu.edu), 4/02/2026
# Description: convert django models into text to send over HTTP
from rest_framework import serializers
from .models import *

class JokeSerializer(serializers.ModelSerializer):
    '''serializer for the joke model. specificies which fields are sent to the API'''

    class Meta:
        model = Joke
        fields = ['joke', 'contributor', 'timestamp']

    #customize create operation
    def create(self, validated_data):
        '''override create superclass method'''
        print(f'JokeSerializer.create, validated_data={validated_data}.')

        return Joke.objects.create(**validated_data)
    
class PictureSerializer(serializers.ModelSerializer):
    '''serializer for the joke model. specificies which fields are sent to the API'''

    class Meta:
        model = Picture
        fields = ['image_url', 'contributor', 'timestamp']

    #customize create operation
    def create(self, validated_data):
        '''override create superclass method'''
        print(f'PictureSerializer.create, validated_data={validated_data}.')

        return Picture.objects.create(**validated_data)