from django.contrib import admin
from django.urls import path
from MyApp import views as myapp_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', myapp_views.HomePage, name='HomePage'),
    path('login/', myapp_views.login_view, name='login'),   # renamed to avoid conflict
    path('signup/', myapp_views.signup_view, name='signup'), # renamed to avoid conflict
    path('logout/', myapp_views.logout_view, name='logout'), # renamed to avoid conflict
]
