from django.contrib import admin
from django.urls import path
from TreeApp import views as treeapp_views

urlpatterns = [
    path('trees/', treeapp_views.TreeProfiles, name = 'TreeProfiles'),
]