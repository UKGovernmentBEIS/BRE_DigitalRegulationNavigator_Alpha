from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Task, TrackedStep, TrackedTask, Tracker


@receiver(m2m_changed, sender=Tracker.regulations.through)
def tracker_regulation_m2m_changed_callback(
    sender, instance, action, model, pk_set, **kwargs
):
    if action == "post_add" and pk_set:
        tasks = Task.objects.filter(regulation__in=pk_set)

        for task in tasks:
            # TODO: Move to model as manager method.
            tracked_task = TrackedTask(
                tracker=instance,
                task=task,
            )
            tracked_task.tracked_steps = [
                TrackedStep(step=step, sort_order=step.sort_order)
                for step in task.steps.all()
            ]
            tracked_task.save()

    elif action == "post_remove" and pk_set:
        # TODO: Soft delete?
        instance.tracked_tasks.filter(task__regulation__in=pk_set).delete()
