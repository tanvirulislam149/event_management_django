from django.shortcuts import render, redirect
from django.contrib import messages
from users.forms import CustomRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator 
from users.forms import CreateGroupForm, ChangeGroupForm



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
        if form.is_valid():
            form.save()
            messages.success(request, "Role created.")
            return redirect("create_group")
    else:
        form = CreateGroupForm()
        return render(request, "admin/create_group.html", {"form": form})
    
def update_group(request, id):
    group = Group.objects.get(id = id)
    if request.method == "POST":
        form = CreateGroupForm(request.POST, instance = group)
        if form.is_valid():
            form.save()
            messages.success(request, "Role updated.")
            return redirect("create_group")
    else:
        form = CreateGroupForm(instance = group)
        return render(request, "admin/create_group.html", {"form": form})

def delete_group(request, id):
    if request.method == "POST":
        group = Group.objects.get(id = id)
        group.delete()
        return redirect("show_group")


def show_group(request):
    groups = Group.objects.all()
    return render(request, "admin/show_groups.html", {"groups": groups})

def change_role(request, id):
    user = User.objects.get(id = id)
    if request.method == "POST":
        form = ChangeGroupForm(request.POST)
        print(user)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            print(role)
            user.groups.clear()
            user.groups.add(role)
            user.save()
            messages.success(request, "Role changed.")
            return redirect("change_role", id)

    else:
        form = ChangeGroupForm()
        return render(request, "admin/change_role.html", {"form": form})