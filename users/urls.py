from django.urls import path
from users.views import register, user_login, user_logout, activate_link, create_group, show_group, update_group, delete_group, change_role, ProfileView, EditProfile, ChangePassword, CustomPasswordResetView, CustomPasswordResetConfirmView
from django.contrib.auth.views import PasswordChangeDoneView


urlpatterns = [
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("activate/<int:user_id>/<str:token>/", activate_link), 
    path("admin/create_group/", create_group, name="create_group"),
    path("admin/show_groups/", show_group, name="show_group"),
    path("admin/update_group/<int:id>", update_group, name="update_group"),
    path("admin/delete_group/<int:id>", delete_group, name="delete_group"),
    path("admin/change_role/<int:id>", change_role, name="change_role"),
    path("user/my_profile", ProfileView.as_view(), name = "my_profile"),
    path("user/edit_profile", EditProfile.as_view(), name = "edit_profile"),
    path("user/change_password", ChangePassword.as_view(), name = "change_password"),
    path("user/change_password_done", PasswordChangeDoneView.as_view(template_name="user/password_change_done.html"), name = "password_change_done"),
    path("user/reset_password", CustomPasswordResetView.as_view(), name = "password_reset"),
    path("user/reset_password_confirm/<uidb64>/<token>/", CustomPasswordResetConfirmView.as_view(), name = "password_reset_confirm"),
]
