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

    path('profile_view/<str:username>/', myapp_views.profile_view, name='profile_view'),  # Profile view


    # Blog app views
    path('blog_list', blogapp_views.blog_list, name='blog_list'),  # Added blog list view
    path('blog_list/<int:pk>/', blogapp_views.blog_detail, name='blog_detail'),  # Detail view
    path('add/', blogapp_views.add_blog, name='add_blog'), #add blog view
    path('edit/<int:pk>/', blogapp_views.edit_blog, name='edit_blog'), #edit blog view
    path('delete/<int:pk>/', blogapp_views.delete_blog, name='delete_blog'), #delete blog view

    # Tree app views
    path('trees/', treeapp_views.TreeProfiles, name = 'TreeProfiles'),# Tree profiles view
    path("dashboard/", treeapp_views.dashboard, name="dashboard"),#user dashboard view
    path("dashboard/ajax/create/", treeapp_views.ajax_create_request, name="ajax_create_request"),#ajax create request view
    path("dashboard/ajax/update/<int:request_id>/", treeapp_views.ajax_update_request, name="ajax_update_request"),#ajax update request view
    path("dashboard/ajax/delete/<int:request_id>/", treeapp_views.ajax_delete_request, name="ajax_delete_request"),#ajax delete request view



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
