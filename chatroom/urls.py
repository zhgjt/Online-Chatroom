"""chatroom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from chat import views

urlpatterns = [
    path('', views.log),
    path('log/', views.log),
    path('signup/', views.signup),
    path('index/', views.index),
    path('get/msg/', views.get_msg),
    path('storage/msg/', views.storage_msg),
    path('get/websocket/', views.get_websocket),
    path('get/allwebsocket/', views.get_allwebsocket),
    path('add/websocket/', views.add_websocket),
    path('delete/websocket/', views.delete_websocket),
]
