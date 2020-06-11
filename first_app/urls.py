from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('adduser', views.adduser),
    path('login', views.login),
    path('wall', views.wall),
    path('destroy', views.destroy),
    path('post_message', views.post_message),	
    path('post_comment/<messageid>', views.post_comment),   
]