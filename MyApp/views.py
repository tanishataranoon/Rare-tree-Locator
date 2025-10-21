from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import SignUpForm, ProfileForm, CustomPasswordChangeForm
from django.contrib.auth import authenticate, login, logout ,update_session_auth_hash
from TreeApp.models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import User, Profile
from django.db.models import Count
from django.urls import reverse
from BlogApp.models import BlogPost, Comment, Notification, Bookmark
from django.contrib.auth import get_user_model
from django.http import JsonResponse


# Home page view
def HomePage(request):
    return render(request, 'HomePage.html')

# Header view
# ##def header(request):
#     return render(request, 'Common/header.html')
# # Footer view
# ##def footer(request):
#     return render(request, 'Common/footer.html')


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

    if user.user_type == "contributor":
        # Contributor sees their trees, posts, and answers
        my_trees = TreeProfile.objects.filter(submitted_by=user)
        posts = BlogPost.objects.filter(author=user)
        # Fetch all answers given by this contributor
        requests = TreeAnswer.objects.filter(answered_by=user).select_related('tree_request')
    else:
        # Common user sees their requests
        my_trees = []  # Not relevant
        requests = TreeRequest.objects.filter(requester=user)

        # Common user sees bookmarked posts
        posts = BlogPost.objects.filter(bookmarked_by__user=user)  # <-- correct query

    context = {
        "profile_user": user,
        "profile": profile,
        "joined_date": joined_date,
        "role": role,
        "my_trees": my_trees,
        "requests": requests,
        "posts": posts,
    }

    # Clear messages
    storage = messages.get_messages(request)
    for _ in storage:
        pass

    return render(request, "Profile/profile_view.html", context)



# Edit profile view
@login_required
def edit_profile(request):
    profile = request.user.profile  # get current user's profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile_view", username=request.user.username)  # ✅ fixed
    else:
        form = ProfileForm(instance=profile)

    context = {
        "form": form
    }
    return render(request, "Profile/edit_profile.html", context)


User = get_user_model()
def user_overview(request):
    users = User.objects.order_by('-date_joined')
    total_users = users.count()
    total_contributors = users.filter(user_type='contributor').count()
    total_common = users.filter(user_type='common').count()

    return render(request, 'Profile/user_overview.html', {
        'users': users,
        'total_users': total_users,
        'total_contributors': total_contributors,
        'total_common': total_common,
    })

