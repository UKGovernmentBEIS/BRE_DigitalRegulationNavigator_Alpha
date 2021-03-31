from django.urls import path

from . import views

app_name = "tracker"

urlpatterns = [
    path("", views.tracker_detail, name="detail"),
    path("create/", views.tracker_create, name="create"),
    path(
        "tasks/<slug:category_slug>/",
        views.tracked_task_list,
        name="tracked-task-list",
    ),
    path(
        "tasks/<slug:category_slug>/<int:pk>/",
        views.tracked_task_detail,
        name="tracked-task-detail",
    ),
    path(
        "tasks/<slug:category_slug>/<int:pk>/complete/",
        views.tracked_task_mark_complete,
        name="tracked-task-mark-complete",
    ),
    path(
        "tasks/<slug:category_slug>/<int:pk>/regulation/",
        views.regulation_detail,
        name="regulation-detail",
    ),
]
