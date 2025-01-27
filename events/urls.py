from django.urls import path
from events.views import dashboard

urlpatterns = [
    path("", dashboard)
]
