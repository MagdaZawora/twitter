from rest_framework import serializers
from .models import Twit, Comment, Message
from django.contrib.auth.models import User

class TwitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Twit
        fields = '__all__'


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('sender', 'receiver', 'content', 'creation_date')
