from django.contrib import admin
from django.urls import path

from . import settings
from django.conf.urls.static import static

from MyApp import views as myapp_views
from TreeApp import views as treeapp_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', myapp_views.HomePage, name='HomePage'),
    path('login/', myapp_views.login_view, name='login'),   # renamed to avoid conflict
    path('signup/', myapp_views.signup_view, name='signup'), # renamed to avoid conflict
    path('logout/', myapp_views.logout_view, name='logout'), # renamed to avoid conflict
    path('TreeProfiles/', treeapp_views.TreeProfiles, name = 'TreeProfiles'),
    #path('header/', myapp_views.header, name='header'), 
    #path('footer/', myapp_views.footer, name='footer'), 
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


