from django.urls import path
from events.views import dashboard, update_event, details, delete_participants, delete_category, accept_invitation, Show_participants, Show_category, Create_event, Create_category, Delete_event

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("show_participants/", Show_participants.as_view(), name="show_participants"),
    path("show_category/", Show_category.as_view(), name="show_category"),
    path("create_event/<int:pageId>/", Create_event.as_view(), name="create_event"),
    path("create_category/<int:pageId>/", Create_category.as_view(), name="create_category"),
    path("create_event/<int:pageId>/<int:eventId>", update_event, name="update_event"),
    path("details/<int:id>", details, name = "details"),
    # path("delete_event/<int:id>", delete_event, name="delete_event"),
    path("delete_event/<int:id>", Delete_event.as_view(), name="delete_event"),
    path("delete_participants/<int:id>", delete_participants, name="delete_participants"),
    path("delete_category/<int:id>", delete_category, name="delete_category"),
    path("accept_invitation/<int:event_id>/", accept_invitation)
]
