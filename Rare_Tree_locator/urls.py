from django.contrib import admin
from django.urls import path, include
from MyApp import views as myapp_views
from TreeApp import views as treeapp_views
from BlogApp import views as blogapp_views  
from DonationApp import views as donationapp_views
from .import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView




urlpatterns = [
    path('', include('TreeApp.urls')),
    path('admin/', admin.site.urls),


    #My app views
    path('', myapp_views.HomePage, name='HomePage'),
    path('signup/', myapp_views.signup_view, name='signup'), 
    path('login/', myapp_views.login_view, name='login'),
    path("logout/", LogoutView.as_view(next_page="HomePage"), name="logout"),
    path('edit_profile/', myapp_views.edit_profile, name="edit_profile"),
    path('profile_view/<str:username>/', myapp_views.profile_view, name='profile_view'),  # Profile view
    path('user-overview/', myapp_views.user_overview, name='user_overview'),


    # Blog app views
    path('blog_list', blogapp_views.blog_list, name='blog_list'),  # Added blog list view
    path('blog_list/<int:pk>/', blogapp_views.blog_detail, name='blog_detail'),  # Detail view
    path('add/', blogapp_views.add_blog, name='add_blog'), #add blog view
    path('edit/<int:pk>/', blogapp_views.edit_blog, name='edit_blog'), #edit blog view
    path('delete/<int:pk>/', blogapp_views.delete_blog, name='delete_blog'), #delete blog view

    path('comment/edit/<int:comment_id>/', blogapp_views.edit_comment, name='edit_comment'),
    path('comment/delete/<int:comment_id>/', blogapp_views.delete_comment, name='delete_comment'),
    path('notifications/mark_read/', blogapp_views.mark_notifications_read, name='mark_notifications_read'),
    path('notifications/mark_read/<int:notif_id>/', blogapp_views.mark_single_notification_read, name='mark_single_notification_read'),
    path('post/<int:post_id>/bookmark/',blogapp_views.toggle_bookmark, name='toggle_bookmark'),

    
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
    path('requests/<int:id>/delete/', treeapp_views.delete_request, name='delete_request'),

    path('requests/<int:pk>/answer/', treeapp_views.answer_request, name='answer_request'),
    path('requests/<int:pk>/answer/view/', treeapp_views.view_submitted_answer, name='view_submitted_answer'),

    path('contact/', treeapp_views.contact, name='contact'),


    # Donation app views
    path('donate/', donationapp_views.initiate_donation, name='donate'),
    path('donate/ipn/', donationapp_views.ssl_ipn, name='ssl_ipn'),
    path('donate/history/', donationapp_views.donation_history, name='donation_history'),
    path('admin/donations/', donationapp_views.admin_donations, name='admin_donations'),
    path('donate/success/', donationapp_views.donate_success, name='donate_success'),  # <-- add this
    path('donate/fail/',donationapp_views.donate_fail, name='donate_fail'),
    path('donate/cancel/',donationapp_views.donate_cancel, name='donate_cancel'),
    path('dashboard/donation-history/', donationapp_views.donation_history_dashboard, name='donation_history_dashboard'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
