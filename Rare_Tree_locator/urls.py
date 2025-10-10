from django.contrib import admin
from django.urls import path, include
from MyApp import views as myapp_views
from TreeApp import views as treeapp_views
from BlogApp import views as blogapp_views  
from .import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView




urlpatterns = [
    path("", include("TreeApp.urls")),
    path('admin/', admin.site.urls),


    #My app views
    path('', myapp_views.HomePage, name='HomePage'),
    path('signup/', myapp_views.signup_view, name='signup'), 
    path('login/', myapp_views.login_view, name='login'),
    path("logout/", LogoutView.as_view(next_page="HomePage"), name="logout"),
    path('edit_profile/', myapp_views.edit_profile, name="edit_profile"),
    path('profile_view/<str:username>/', myapp_views.profile_view, name='profile_view'),  # Profile view

    # Blog app views
    path('blog_list', blogapp_views.blog_list, name='blog_list'),  # Added blog list view
    path('blog_list/<int:pk>/', blogapp_views.blog_detail, name='blog_detail'),  # Detail view
    path('add/', blogapp_views.add_blog, name='add_blog'), #add blog view
    path('edit/<int:pk>/', blogapp_views.edit_blog, name='edit_blog'), #edit blog view
    path('delete/<int:pk>/', blogapp_views.delete_blog, name='delete_blog'), #delete blog view

    # Tree app views
    path('trees/', treeapp_views.TreeProfiles, name = 'TreeProfiles'),# Tree profiles view
    path('map/', treeapp_views.map_page, name='map_page'),
    path('add-tree-ajax/', treeapp_views.add_tree_ajax, name='add_tree_ajax'),
    path('api/trees/', treeapp_views.get_trees_json, name='get_trees_json'),
    
    path("dashboard/", treeapp_views.dashboard, name="dashboard"),#user dashboard view
    path('tree-requests/', treeapp_views.tree_requests, name='tree_requests'),

    path("requests/", treeapp_views.request_list, name="request_list"),
    path("requests/create/", treeapp_views.create_request, name="create_request"),
    path("requests/<int:pk>/detail/", treeapp_views.request_detail_ajax, name="request_detail_ajax"),
    path('requests/<int:id>/delete/', treeapp_views.delete_request, name='delete_request')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
