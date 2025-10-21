from django.contrib import admin
from django.urls import path
from TreeApp import views as treeapp_views
from . import views

urlpatterns = [
    path('trees/', treeapp_views.TreeProfiles, name = 'TreeProfiles'),
    path('tree/<int:pk>/', views.tree_detail, name='tree_detail'),
    path('map/', treeapp_views.map_page, name='map_page'),
    path('add-tree-ajax/', treeapp_views.add_tree_ajax, name='add_tree_ajax'),
    path('api/trees/', treeapp_views.get_trees_json, name='get_trees_json'),
    path('contact/', treeapp_views.contact, name='contact'),
] 

