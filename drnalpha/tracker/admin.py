from django.contrib import admin

from .models import Step, Task, TrackedStep, TrackedTask, Tracker, TrackerRegulation


class StepInline(admin.StackedInline):
    model = Step
    extra = 0


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    autocomplete_fields = ["regulation"]
    inlines = [StepInline]
    list_display = ["name", "updated_at"]
    search_fields = ["name"]


class TrackerRegulationInline(admin.TabularInline):
    autocomplete_fields = ["regulation"]
    extra = 0
    model = TrackerRegulation


@admin.register(Tracker)
class TrackerAdmin(admin.ModelAdmin):
    autocomplete_fields = ["user", "company"]
    inlines = [TrackerRegulationInline]
    list_display = ["company", "updated_at"]
    search_fields = ["company__name"]


class TrackedStepInline(admin.StackedInline):
    extra = 0
    fields = ["step", "due_date", "status"]
    model = TrackedStep
    readonly_fields = ["step"]

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(TrackedTask)
class TrackedTaskAdmin(admin.ModelAdmin):
    fields = ["tracker", "task", "status"]
    inlines = [TrackedStepInline]
    list_display = ["task", "tracker", "updated_at"]
    list_filter = ["status"]
    readonly_fields = ["tracker", "task"]

    def has_add_permission(self, request, obj=None):
        return False
