from django.urls import path
from users.views import register, user_login, user_logout, activate_link, create_group, show_group, update_group, delete_group, change_role, ProfileView, EditProfile, ChangePassword

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
    path("user/change_password", ChangePassword.as_view(), name = "change_password")
]
