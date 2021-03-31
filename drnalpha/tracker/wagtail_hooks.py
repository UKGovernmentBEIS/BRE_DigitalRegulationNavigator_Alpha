from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from drnalpha.companies.models import Company

from .models import Task, TrackedTask, Tracker


class CompanyAdmin(ModelAdmin):
    model = Company
    list_display = ["__str__"]
    menu_icon = "group"
    ordering = ["name", "pk"]
    search_fields = ["name"]


class TaskAdmin(ModelAdmin):
    model = Task
    list_display = ["name", "regulation", "updated_at"]
    menu_icon = "tasks"
    ordering = ["name"]
    search_fields = ["name"]


class TrackerAdmin(ModelAdmin):
    model = Tracker
    inspect_view_enabled = True
    inspect_template_name = "patterns/pages/modeladmin/tracker/tracker/inspect.html"
    list_display = ["company", "updated_at"]
    menu_icon = "view"
    ordering = ["-updated_at"]
    search_fields = ["company__name"]


class TrackedTaskAdmin(ModelAdmin):
    model = TrackedTask
    inspect_view_enabled = True
    inspect_template_name = (
        "patterns/pages/modeladmin/tracker/tracked_task/inspect.html"
    )
    list_display = ["task", "tracker", "updated_at"]
    menu_icon = "tasks"
    ordering = ["task"]


class TrackerAdminGroup(ModelAdminGroup):
    menu_label = "Tracker"
    menu_icon = "tasks"
    menu_order = 512
    items = [CompanyAdmin, TaskAdmin, TrackerAdmin, TrackedTaskAdmin]


modeladmin_register(TrackerAdminGroup)
