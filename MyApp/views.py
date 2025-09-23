from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from TreeApp.models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import User, Profile
from django.urls import reverse
from BlogApp.models import BlogPost
# Home page view
def HomePage(request):
    return render(request, 'HomePage.html')
# Header view
##def header(request):
    return render(request, 'Common/header.html')
# Footer view
##def footer(request):
    return render(request, 'Common/footer.html')
# Signup view
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect("login")
    else:
        form = SignUpForm()
    return render(request, "Profile/signup.html", {"form": form})
# Login view
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Redirect straight to profile page
            return redirect(reverse("profile_view", kwargs={"username": user.username}))
            
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "Profile/login.html")
#profile view
@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile  

    joined_date = profile.joined_date
    role = user.get_user_type_display()

    # Role-specific logic
    if user.user_type == "contributor":
        my_trees = TreeProfile.objects.filter(submitted_by=user)
        requests = []  # to be replaced when you build Request model
        posts = BlogPost.objects.filter(author=user)
    else:  # common user
        my_trees = []  # future: trees added because of requests
        requests = []  # future: request history
        posts = []     # future: saved/liked posts

    context = {
        "profile_user": user,
        "profile": profile,
        "joined_date": joined_date,
        "role": role,
        "my_trees": my_trees,
        "requests": requests,
        "posts": posts,
    }
    return render(request, "Profile/profile_view.html", context)
