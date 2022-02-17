from django.urls import path
from . import views

urlpatterns = [
    path('chatCredentialsCheck', views.chatCredentialsCheck, name='chatCredentialsCheck'),
    path('prevMsgs', views.prevMsgs, name='prevMsgs'),
]
