from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
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
# Signup view
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get("full_name")
            user.save()
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

            # Redirect based on user_type
            if user.user_type == "contributor":
                return redirect("contributor_dashboard")
            elif user.user_type == "common":
                return redirect("home")
            elif user.user_type == "admin":
                return redirect("admin_dashboard")
            else:
                return redirect("home")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "Profile/login.html")