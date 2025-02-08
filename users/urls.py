from django.urls import path
from users.views import register, user_login, user_logout, activate_link

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("activate/<int:user_id>/<str:token>/", activate_link)
]
