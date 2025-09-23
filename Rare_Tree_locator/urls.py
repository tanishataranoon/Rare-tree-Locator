from django.contrib import admin
from django.urls import path, include
from MyApp import views as myapp_views
from TreeApp import views as treeapp_views
from BlogApp import views as blogapp_views  
from .import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", include("TreeApp.urls")),
    path('admin/', admin.site.urls),
    path('', myapp_views.HomePage, name='HomePage'),
    path('signup/', myapp_views.signup_view, name='signup'), 
    path('login/', myapp_views.login_view, name='login'),
    path('blog_list', blogapp_views.blog_list, name='blog_list'),  # Added blog list view
    path('blog_list/<int:pk>/', blogapp_views.blog_detail, name='blog_detail'),  # Detail view
    path('profile_view/<str:username>/', myapp_views.profile_view, name='profile_view'),  # Profile view
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
