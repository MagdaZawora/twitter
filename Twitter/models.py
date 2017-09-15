from django.db import models
from Twitter import admin
from django.contrib import admin
from django.forms import widgets
from django.utils import timezone
from django.contrib.auth.models import User


# class TwitUser(models.Model):
#     first_name = models.CharField(max_length=64)
#     last_name = models.CharField(max_length=64)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=64, null=True)
#     password2 = models.CharField(max_length=64, null=True)
#
#     def __str__(self):
#         return '{} {}'.format(self.first_name, self.last_name)
#
# admin.site.register(TwitUser)


class Twit(models.Model):
    content_twit = models.CharField(max_length=140)
    creation_date = models.DateTimeField(default=timezone.now)
    author_twit = models.ForeignKey(User)

    def __str__(self):
        return 'Twit by {} @ {}: "{}..."'.format(self.author_twit,
                                                  self.creation_date,
                                                  str(self.content_twit)[:32])
admin.site.register(Twit)


class Comment(models.Model):
    content_comment = models.CharField(max_length=60)
    author_comment = models.ForeignKey(User)
    relating_to = models.ForeignKey(Twit)
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content_comment

admin.site.register(Comment)


class Message(models.Model):
    sender = models.ForeignKey(User)
    receiver = models.ForeignKey(User, related_name="message_receiver")
    content = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return 'Message from {} to {} @ {}'.format(self.sender, self.receiver, self.creation_date)

admin.site.register(Message)

