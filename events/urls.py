from django.urls import path
from events.views import dashboard, create_event, update_event, details, delete_event, delete_participants, delete_category, accept_invitation, Show_participants, Show_category

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("show_participants/", Show_participants.as_view(), name="show_participants"),
    path("show_category/", Show_category.as_view(), name="show_category"),
    path("create_event/<int:pageId>/", create_event, name="create_event"),
    path("create_event/<int:pageId>/<int:eventId>", update_event, name="update_event"),
    path("details/<int:id>", details, name = "details"),
    path("delete_event/<int:id>", delete_event, name="delete_event"),
    path("delete_participants/<int:id>", delete_participants, name="delete_participants"),
    path("delete_category/<int:id>", delete_category, name="delete_category"),
    path("accept_invitation/<int:event_id>/", accept_invitation)
]
