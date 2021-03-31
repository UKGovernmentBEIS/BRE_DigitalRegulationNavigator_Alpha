from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST

from drnalpha.finder.decorators import FINDER_DATA_KEY, finder_data_required
from drnalpha.finder.forms import CompanyForm
from drnalpha.users.forms import RegistrationForm
from drnalpha.utils.notify import send_notify_email

from .decorators import category_required, tracker_required
from .forms import TrackedTaskFilterForm
from .models import Tracker


@finder_data_required
@transaction.atomic
def tracker_create(request, finder_data):
    if hasattr(request.user, "tracker"):
        return redirect("tracker:detail")

    if request.method == "POST":
        form = RegistrationForm(data=request.POST)

        if form.is_valid():
            user = form.save()

            company_form = CompanyForm.for_finder_data(finder_data)
            company = company_form.save()

            tracker = Tracker.objects.create_for_user_and_company(
                user=user, company=company
            )

            del request.session[FINDER_DATA_KEY]

            messages.success(
                request,
                "Your tracker has been created. Please sign in to continue.",
            )

            send_welcome_email(request, user=user, tracker=tracker)

            return redirect("tracker:detail")
    else:
        form = RegistrationForm()

    return TemplateResponse(
        request, "patterns/pages/tracker/tracker_create.html", {"form": form}
    )


def send_welcome_email(request, *, user, tracker):
    context = {
        "user": user,
        "tracker": tracker,
    }

    subject = render_to_string(
        template_name="patterns/pages/tracker/welcome_email_subject.txt",
        context=context,
        request=request,
    )
    # Force subject to a single line to avoid header-injection
    # issues.
    subject = "".join(subject.splitlines())

    message = render_to_string(
        template_name="patterns/pages/tracker/welcome_email_body.txt",
        context=context,
        request=request,
    )

    if not send_notify_email(user.email, subject, message):
        html_message = render_to_string(
            template_name="patterns/pages/tracker/welcome_email_body.html",
            context=context,
            request=request,
        )
        user.email_user(subject, message, html_message=html_message)


@login_required()
@tracker_required()
def tracker_detail(request, tracker):
    return TemplateResponse(
        request,
        "patterns/pages/tracker/tracker_detail.html",
        {
            "tracker": tracker,
        },
    )


@login_required()
@tracker_required()
@category_required()
def tracked_task_list(request, tracker, category):
    tracked_tasks = tracker.get_tracked_tasks().for_category(category)

    data = request.GET if bool(request.GET) else None
    form = TrackedTaskFilterForm(data, queryset=tracked_tasks)

    if form.is_valid():
        tracked_tasks = form.get_filtered_queryset()
        form = TrackedTaskFilterForm(data, queryset=tracked_tasks)

    return TemplateResponse(
        request,
        "patterns/pages/tracker/tracked_task_list.html",
        {
            "tracker": tracker,
            "category": category,
            "form": form,
            "tasks": tracked_tasks,
        },
    )


@login_required()
@tracker_required()
@category_required()
def tracked_task_detail(request, tracker, category, pk):
    tracked_task = get_object_or_404(tracker.get_tracked_tasks(), pk=pk)

    return TemplateResponse(
        request,
        "patterns/pages/tracker/tracked_task_detail.html",
        {
            "tracker": tracker,
            "category": category,
            "task": tracked_task,
        },
    )


@require_POST
@login_required()
@tracker_required()
def tracked_task_mark_complete(request, tracker, category_slug, pk):
    tracked_task = get_object_or_404(tracker.get_tracked_tasks(), pk=pk)

    tracked_task.mark_complete()

    messages.success(request, "Your task has been completed!")
    return redirect("tracker:tracked-task-detail", category_slug, pk)


@login_required()
@tracker_required()
@category_required()
def regulation_detail(request, tracker, category, pk):
    tracked_task = get_object_or_404(tracker.get_tracked_tasks(), pk=pk)
    regulation = tracked_task.regulation
    tracked_tasks_count = tracker.get_tracked_tasks().for_regulation(regulation).count()
    completed_tasks_count = (
        tracker.get_tracked_tasks().for_regulation(regulation).complete().count()
    )

    return TemplateResponse(
        request,
        "patterns/pages/tracker/regulation_detail.html",
        {
            "tracker": tracker,
            "category": category,
            "task": tracked_task,
            "regulation": regulation,
            "tasks_count": tracked_tasks_count,
            "completed_tasks_count": completed_tasks_count,
            "outstanding_tasks_count": tracked_tasks_count - completed_tasks_count,
        },
    )
