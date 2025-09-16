from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from TreeApp.models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# Home page view
def HomePage(request):
    return render(request, 'HomePage.html')
  
# Header view
##def header(request):
    return render(request, 'Common/header.html')
# Footer view
##def footer(request):
    return render(request, 'Common/footer.html')
# Login view
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)   # ✅ use Django's login function
            return redirect("home")     # make sure you have a URL name 'home'
    else:
        form = AuthenticationForm()
    
    signup_form = UserCreationForm()  # For popup modal
    return render(request, "MyApp/login.html", {"form": form, "signup_form": signup_form})

# Signup view
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)   # ✅ same fix here
            return redirect("home")
    return redirect("login")  # fallback

# Logout view
def logout_view(request):
    auth_logout(request)   # ✅ call Django's logout
    return redirect("login")
