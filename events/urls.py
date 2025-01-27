from django.urls import path
from events.views import dashboard, create_event

urlpatterns = [
    path("", dashboard),
    path("create_event/", create_event, name="create_event")
]
