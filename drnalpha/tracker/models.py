from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable

from wagtailautocomplete.edit_handlers import AutocompletePanel

from drnalpha.companies.models import Company
from drnalpha.regulations.models import Category, Regulation


class TrackerManager(models.Manager):
    def create_for_user_and_company(self, *, user, company):
        tracker = self.create(user=user, company=company)
        tracker.regulations.set(self.get_initial_regulations(company))
        return tracker

    # TODO: Could move to the company model as it currently only uses company info.
    def get_initial_regulations(self, company):
        return (
            Regulation.objects.for_jurisdictions(company.jurisdictions.all())
            .for_sic_codes(company.sic_codes.all())
            .distinct("name")
        )


class Tracker(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    company = models.OneToOneField(
        Company, on_delete=models.PROTECT, related_name="tracker"
    )
    regulations = models.ManyToManyField(
        "regulations.Regulation",
        related_name="trackers",
        through="TrackerRegulation",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TrackerManager()

    panels = [
        FieldPanel("user"),
        FieldPanel("company"),
        AutocompletePanel("regulations"),
    ]

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.company} tracker"

    def get_categories(self):
        regulations = self.regulations.all()
        return Category.objects.filter(regulations__in=regulations).distinct("name")

    # TODO: Should these be tasks not regulations?
    def get_categories_with_regulations_count(self):
        return (
            self.get_categories()
            .with_regulations_count()
            .order_by("name")
            .distinct("name")
        )

    def get_tracked_tasks(self):
        return self.tracked_tasks.all().select_related("task", "task__regulation")


class TrackerRegulation(models.Model):
    tracker = models.ForeignKey(
        Tracker,
        on_delete=models.CASCADE,
        related_name="tracker_regulations",
    )
    regulation = models.ForeignKey(
        Regulation,
        on_delete=models.CASCADE,
        related_name="tracker_regulations",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.tracker}: {self.regulation}"


class Task(ClusterableModel):
    # Compliance task and steps were explored as part of initial Tracker work.
    # There were dropped for the MVP but have been left in as they could form part
    # of the future service.
    name = models.CharField(max_length=255)
    description = RichTextField(blank=True)
    regulation = models.ForeignKey(
        Regulation, on_delete=models.CASCADE, related_name="tasks"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        AutocompletePanel("regulation"),
        InlinePanel("steps", label="Steps"),
    ]

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.name


class Step(Orderable):
    task = ParentalKey(Task, on_delete=models.CASCADE, related_name="steps")
    name = models.CharField(max_length=255)
    description = RichTextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]

    def __str__(self):
        return self.name


class Status(models.IntegerChoices):
    NOT_STARTED = 0, "Not started"
    IN_PROGRESS = 1, "In progress"
    COMPLETE = 2, "Complete"
    DUE = 3, "Due"  # TODO: Infer from step is_due?
    OVERDUE = 4, "Overdue"  # TODO: Infer from step is_overdue?


class TrackedTaskQuerySet(models.QuerySet):
    def outstanding(self):
        return self.exclude(status=Status.COMPLETE)

    def complete(self):
        return self.filter(status=Status.COMPLETE)

    def for_regulation(self, regulation):
        return self.filter(task__regulation=regulation)

    def for_category(self, category):
        return self.filter(task__regulation__categories=category)


class TrackedTask(ClusterableModel):
    tracker = models.ForeignKey(
        Tracker, on_delete=models.PROTECT, related_name="tracked_tasks"
    )
    task = models.ForeignKey(
        Task, on_delete=models.PROTECT, related_name="tracked_tasks"
    )
    status = models.IntegerField(
        choices=Status.choices, db_index=True, default=Status.NOT_STARTED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel("tracker"),
        FieldPanel("task"),
        FieldPanel("status"),
        InlinePanel("tracked_steps", label="Steps"),
    ]

    objects = TrackedTaskQuerySet.as_manager()

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.task.name

    def get_tracked_steps(self):
        return self.tracked_steps.all().select_related("step")

    def mark_complete(self, commit=True):
        if not self.is_complete:
            self.status = Status.COMPLETE
            if commit:
                self.save(update_fields=["status", "updated_at"])

    @property
    def name(self):
        return self.task.name

    @property
    def company(self):
        return self.tracker.company

    @property
    def description(self):
        return self.task.description

    @property
    def regulation(self):
        return self.task.regulation

    @property
    def is_complete(self):
        return self.status == Status.COMPLETE


class TrackedStep(Orderable):
    tracked_task = ParentalKey(
        TrackedTask, on_delete=models.CASCADE, related_name="tracked_steps"
    )
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name="+")
    due_date = models.DateField(null=True, blank=True)
    status = models.IntegerField(
        choices=Status.choices, db_index=True, default=Status.NOT_STARTED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel("step"),
        FieldPanel("due_date"),
        FieldPanel("status"),
    ]

    def __str__(self):
        return self.step.name

    @property
    def name(self):
        return self.step.name

    @property
    def description(self):
        return self.step.description

    @property
    def is_due(self):
        return (
            self.status != Status.COMPLETE
            and self.due_date
            and self.due_date < timezone.now().date() + timedelta(weeks=1)
        )

    @property
    def is_overdue(self):
        return (
            self.status != Status.COMPLETE
            and self.due_date
            and self.due_date < timezone.now().date()
        )
