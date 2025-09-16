from django.contrib import admin
from django.urls import path, include
from MyApp import views as myapp_views
from .import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", include("TreeApp.urls")),
    path('admin/', admin.site.urls),
    path('', myapp_views.HomePage, name='HomePage'),
    path('blog/', myapp_views.blog, name='blog'),
    path('login/', myapp_views.login_view, name='login'),   # renamed to avoid conflict
    path('signup/', myapp_views.signup_view, name='signup'), # renamed to avoid conflict
    path('logout/', myapp_views.logout_view, name='logout'), # renamed to avoid conflict
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
