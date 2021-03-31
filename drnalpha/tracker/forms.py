from django import forms

from crispy_forms.helper import FormHelper

from drnalpha.regulations.models import Importance, Jurisdiction, Regulation

from .models import Status


class TrackedTaskFilterForm(forms.Form):
    FILTERS = {
        "importance": "task__regulation__importance__in",
        "jurisdiction": "task__regulation__jurisdictions__in",
        "status": "status__in",
        "regulations": "task__regulation__in",
    }

    importance = forms.TypedMultipleChoiceField(
        choices=[],
        coerce=int,
        required=False,
        widget=forms.widgets.CheckboxSelectMultiple,
    )
    jurisdiction = forms.ModelMultipleChoiceField(
        label="Location",
        queryset=None,
        required=False,
        widget=forms.widgets.CheckboxSelectMultiple,
    )
    status = forms.TypedMultipleChoiceField(
        choices=[],
        coerce=int,
        required=False,
        widget=forms.widgets.CheckboxSelectMultiple,
    )
    regulations = forms.ModelMultipleChoiceField(
        queryset=None,
        required=False,
        widget=forms.widgets.CheckboxSelectMultiple,
    )

    def __init__(self, data, *, queryset):
        self.queryset = queryset

        super().__init__(data)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.checkboxes_small = True
        self.helper.hide_label = True  # custom setting

        self.fields["importance"].choices = self.get_importance_choices()
        self.fields["jurisdiction"].queryset = self.get_jurisdiction_queryset()
        self.fields["status"].choices = self.get_status_choices()
        self.fields["regulations"].queryset = self.get_regulations_queryset()

    def get_importance_choices(self):
        values = (
            self.queryset.values_list("task__regulation__importance", flat=True)
            .distinct()
            .order_by("task__regulation__importance")
        )
        return [(value, Importance(value).label) for value in values]

    def get_jurisdiction_queryset(self):
        return Jurisdiction.objects.filter(
            regulations__tasks__tracked_tasks__in=list(self.queryset)
        ).distinct()

    def get_status_choices(self):
        values = (
            self.queryset.values_list("status", flat=True).distinct().order_by("status")
        )
        return [(value, Status(value).label) for value in values]

    def get_regulations_queryset(self):
        return Regulation.objects.filter(
            tasks__tracked_tasks__in=list(self.queryset)
        ).distinct()

    def get_filtered_queryset(self):
        filters = {}

        for key in self.data.keys():
            lookup = self.FILTERS.get(key)
            value = self.cleaned_data.get(key)

            if lookup and value:
                filters[lookup] = value

        return self.queryset.filter(**filters).distinct()
