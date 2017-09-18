"""myTwitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Twitter.views import HomeView, UserTwitsView, TwitView, LogoutView, \
    ResetPasswordView, MessageView, NewMessageView, UserMessagesView, AddUserView, LoginView
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/(?P<id>\d+)/$', HomeView.as_view(), name='home'),
    url(r'^user_twits/(?P<id>\d+)/$', UserTwitsView.as_view(), name='user_twits'),
    url(r'^details_twit/(?P<id>\d+)/$', TwitView.as_view(), name='details_twit'),
    url(r'^login/$', LoginView.as_view() ,name='login'),
    url(r'^logout/(?P<id>\d+)/$', LogoutView.as_view(), name='logout'),
    url(r'^add_user/$', AddUserView.as_view(), name='add_user'),
    url(r'^reset_password/(?P<id>\d+)/$', ResetPasswordView.as_view(), name='reset_password'),
    url(r'^details_message/(?P<id>\d+)/$', MessageView.as_view(), name='details_message'),
    url(r'^new_message/(?P<id>\d+)/?$', NewMessageView.as_view(), name='new_message'),
    url(r'^user_messages/(?P<id>\d+)/?$', UserMessagesView.as_view(), name='user_messages'),

]