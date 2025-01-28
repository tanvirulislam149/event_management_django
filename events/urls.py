from django.urls import path
from events.views import dashboard, create_event, update_event

urlpatterns = [
    path("dashboard/", dashboard),
    path("create_event/<int:pageId>/", create_event, name="create_event"),
    path("create_event/<int:pageId>/<int:eventId>", update_event, name="update_event")
]
