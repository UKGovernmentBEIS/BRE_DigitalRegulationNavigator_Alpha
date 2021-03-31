from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout

from drnalpha.companies.models import Company
from drnalpha.regulations.models import Category, Importance, Jurisdiction, Regulation
from drnalpha.sic_codes.models import Code


class FinderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

    def clean(self):
        # Any QuerySet values from cleaned ModelMultipleChoice fields can't be stored
        # in the session as is. Here we call custom dump_<fieldname>() methods to
        # convert them into something that can, such as list of primary keys.

        self.dumped_data = {}

        if self.cleaned_data:
            for name, value in self.cleaned_data.items():
                if hasattr(self, f"dump_{name}"):
                    value = getattr(self, f"dump_{name}")()
                self.dumped_data[name] = value


# class InfoForm(FinderForm, forms.ModelForm):
#     class Meta:
#         model = Company
#         fields = ["name", "postal_code"]
#         labels = {
#             "name": "What is your company name?",
#             "postcal_code": "What is your postal code?",
#         }
#         widgets = {
#             "name": forms.widgets.TextInput(attrs={"autocomplete": "organisation"}),
#             "postcal_code": forms.widgets.TextInput(
#                 attrs={"autocomplete": "postal-code"}
#             ),
#         }


class LocationsForm(FinderForm, forms.ModelForm):
    class Meta:
        model = Company
        fields = ["jurisdictions"]
        labels = {
            "jurisdictions": "Where does your business operate?",
        }
        widgets = {
            "jurisdictions": forms.widgets.CheckboxSelectMultiple,
        }

    def dump_jurisdictions(self):
        data = self.cleaned_data["jurisdictions"]
        if data:
            return list(data.values_list("pk", flat=True))
        return []


class EmployeesForm(FinderForm, forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            "full_time_permanent_employees",
            "full_time_contract_employees",
            "part_time_permanent_employees",
            "part_time_contract_employees",
        ]
        labels = {
            "full_time_permanent_employees": "Permanent",
            "full_time_contract_employees": "Contract",
            "part_time_permanent_employees": "Permanent",
            "part_time_contract_employees": "Contract",
        }
        widgets = {
            "full_time_permanent_employees": forms.widgets.TextInput(
                attrs={
                    "pattern": "[0-9]*",
                    "inputmode": "numeric",
                    "class": "govuk-input govuk-input--width-4",
                }
            ),
            "full_time_contract_employees": forms.widgets.TextInput(
                attrs={
                    "pattern": "[0-9]*",
                    "inputmode": "numeric",
                    "class": "govuk-input govuk-input--width-4",
                }
            ),
            "part_time_permanent_employees": forms.widgets.TextInput(
                attrs={
                    "pattern": "[0-9]*",
                    "inputmode": "numeric",
                    "class": "govuk-input govuk-input--width-4",
                }
            ),
            "part_time_contract_employees": forms.widgets.TextInput(
                attrs={
                    "pattern": "[0-9]*",
                    "inputmode": "numeric",
                    "class": "govuk-input govuk-input--width-4",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.labels_small = True
        self.helper.layout = Layout(
            Fieldset(
                "How many people do you employ full-time?",
                "full_time_permanent_employees",
                "full_time_contract_employees",
            ),
            Fieldset(
                "How many people do you employ part-time?",
                "part_time_permanent_employees",
                "part_time_contract_employees",
            ),
        )


class ActivityModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.title


class ActivitiesForm(FinderForm, forms.ModelForm):
    sic_codes = ActivityModelMultipleChoiceField(
        label="Which of these activities describes what your business does?",
        queryset=Code.objects.related_to_food(),
        required=True,
        widget=forms.widgets.CheckboxSelectMultiple,
    )

    class Meta:
        model = Company
        fields = ["sic_codes"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.checkboxes_small = True
        self.helper.checkboxes_columns = True

    def dump_sic_codes(self):
        data = self.cleaned_data["sic_codes"]
        if data:
            return list(data.values_list("pk", flat=True))
        return []


class ReviewForm(FinderForm):
    pass


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            "name",
            "jurisdictions",
            "full_time_permanent_employees",
            "full_time_contract_employees",
            "part_time_permanent_employees",
            "part_time_contract_employees",
            "sic_codes",
        ]

    @classmethod
    def for_finder_data(cls, data):
        flattened_data = {}
        for item in data.values():
            flattened_data.update(item)

        return cls(data=flattened_data)


class RegulationFinderForm(FinderForm, CompanyForm):
    def __init__(self, data, *args, **kwargs):
        self.queryset = Regulation.objects.all()
        super().__init__(data, *args, **kwargs)

    def get_filtered_queryset(self):
        return (
            self.queryset.for_jurisdictions(self.cleaned_data["jurisdictions"])
            .for_sic_codes(self.cleaned_data["sic_codes"])
            .distinct()
        )


class RegulationFilterForm(FinderForm):
    FILTERS = {
        "importance": "importance__in",
        "jurisdiction": "jurisdictions__in",
        "category": "categories__in",
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
        to_field_name="slug",
        widget=forms.widgets.CheckboxSelectMultiple,
    )
    category = forms.ModelMultipleChoiceField(
        queryset=None,
        required=False,
        to_field_name="slug",
        widget=forms.widgets.CheckboxSelectMultiple,
    )

    def __init__(self, data, *, queryset):
        self.queryset = queryset

        super().__init__(data)

        self.helper.checkboxes_small = True
        self.helper.hide_label = True  # custom setting

        self.fields["importance"].choices = self.get_importance_choices()
        self.fields["jurisdiction"].queryset = self.get_jurisdiction_queryset()
        self.fields["category"].queryset = self.get_category_queryset()

    def get_importance_choices(self):
        values = (
            self.queryset.values_list("importance", flat=True)
            .distinct()
            .order_by("importance")
        )
        return [(value, Importance(value).label) for value in values]

    def get_jurisdiction_queryset(self):
        return (
            Jurisdiction.objects.filter(regulations__in=list(self.queryset))
            .distinct()
            .order_by("name")
        )

    def get_category_queryset(self):
        return (
            Category.objects.filter(regulations__in=list(self.queryset))
            .distinct()
            .order_by("name")
        )

    def get_filtered_queryset(self):
        filters = {}

        for key in self.data.keys():
            lookup = self.FILTERS.get(key)
            value = self.cleaned_data.get(key)

            if lookup and value:
                filters[lookup] = value

        return self.queryset.filter(**filters).distinct()
