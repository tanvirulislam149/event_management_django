from django.shortcuts import render, redirect
from django.contrib import messages
from users.forms import CustomRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator 
from users.forms import CreateGroupForm, ChangeGroupForm, EditCustomUserForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomPasswordResetConfirmForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import TemplateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView, PasswordChangeDoneView
from decouple import config


User = get_user_model() 



def is_admin(user):
    return user.groups.filter(name="Admin").exists()


def is_organizer_or_admin(user):
    return user.groups.filter(name="Organizer").exists() or user.groups.filter(name="Admin").exists()


# Create your views here.

def dashboard_redirect(request):
    if is_admin(request.user):
        return redirect("dashboard")
    elif is_organizer_or_admin(request.user):
        return redirect("organizer_dashboard")
    else:
        return redirect("user_dashboard")


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
            next_url = request.GET.get("next")
            return redirect(f"{config('FRONTEND_URL')}{next_url}") if next_url else redirect("home")
        else:
            messages.error(request, "Wrong credentials. Please check again.")


    return render(request, "login.html")

@login_required
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
    
@login_required
@user_passes_test(is_admin, "no_permission")
def create_group(request):
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Role created.")
            return redirect("create_group")
    else:
        form = CreateGroupForm()
        context = {
            "form": form,
            "is_admin": is_admin(request.user),
            "is_organizer": is_organizer_or_admin(request.user),
        }
        return render(request, "admin/create_group.html", context)
    
@login_required
@user_passes_test(is_admin, "no_permission")
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
        context = {
            "form": form,
            "is_admin": is_admin(request.user),
            "is_organizer": is_organizer_or_admin(request.user),
        }
        return render(request, "admin/create_group.html", context)

@login_required
@user_passes_test(is_admin, "no_permission")
def delete_group(request, id):
    if request.method == "POST":
        group = Group.objects.get(id = id)
        group.delete()
        return redirect("show_group")


@login_required
@user_passes_test(is_admin, "no_permission")
def show_group(request):
    groups = Group.objects.prefetch_related("permissions").all()
    context = {
        "groups": groups,
        "is_admin": is_admin(request.user),
        "is_organizer": is_organizer_or_admin(request.user),
    }
    return render(request, "admin/show_groups.html", context)

@login_required
@user_passes_test(is_admin, "no_permission")
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
        context = {
            "form": form,
            "is_admin": is_admin(request.user),
            "is_organizer": is_organizer_or_admin(request.user),
        }
        return render(request, "admin/change_role.html", context)
    

@method_decorator(login_required, name="dispatch")
class ProfileView(TemplateView):
    template_name = "user/my_profile.html"

    def get_context_data(self, **kwargs):
        user = self.request.user 
        context = super().get_context_data(**kwargs)
        context["user"] = user
        context["is_admin"] = is_admin(self.request.user)
        context["is_organizer"] = is_organizer_or_admin(self.request.user)
        return context 
    
class EditProfile(UpdateView):
    model = User
    template_name = "user/edit_profile.html"
    form_class = EditCustomUserForm
    success_url = reverse_lazy("edit_profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_admin"] = is_admin(self.request.user)
        context["is_organizer"] = is_organizer_or_admin(self.request.user)
        return context 
    
    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect("edit_profile")
    

class ChangePassword(PasswordChangeView):
    template_name = "user/change_password.html"
    form_class = CustomPasswordChangeForm

    def get_context_data(self, **kwargs):
            # user = self.request.user 
            context = super().get_context_data(**kwargs)
            context["is_admin"] = is_admin(self.request.user)
            context["is_organizer"] = is_organizer_or_admin(self.request.user)
            return context 


class ChangePasswordDoneView(PasswordChangeDoneView):
    template_name = "user/password_change_done.html"

    def get_context_data(self, **kwargs):
            # user = self.request.user 
            context = super().get_context_data(**kwargs)
            context["is_admin"] = is_admin(self.request.user)
            context["is_organizer"] = is_organizer_or_admin(self.request.user)
            return context 


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'user/reset_password.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context

    def form_valid(self, form):
        messages.success(
            self.request, 'Password reset email is sent. Please check your email.')
        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'user/reset_password.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(
            self.request, 'Password reset successfully')
        return super().form_valid(form)

