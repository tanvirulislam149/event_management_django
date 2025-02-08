from django.shortcuts import render, redirect
from django.contrib import messages
from users.forms import CustomRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator 
from users.forms import CreateGroupForm



# Create your views here.
def register(request):
    form = CustomRegisterForm()
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            messages.success(request, "User created successfully. Please check your email for activation link.")
            return redirect("register")
    
    return render(request, "register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Wrong credentials. Please check again.")


    return render(request, "login.html")

def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")
    
def activate_link(request, user_id, token):
    user = User.objects.get(id = user_id)
    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Account activated. Please login. ")
        return redirect("login")
    else:
        return render("Invalid token or id")
    
def create_group(request):
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid:
            form.save()
            messages.success(request, "Role created.")
            return redirect("create_group")
    else:
        form = CreateGroupForm()
        return render(request, "admin/create_group.html", {"form": form})