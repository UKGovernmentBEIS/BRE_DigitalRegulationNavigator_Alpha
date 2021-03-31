from django.db import models
from django.forms.widgets import CheckboxSelectMultiple

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel

from wagtailautocomplete.edit_handlers import AutocompletePanel

from drnalpha.regulations.models import Jurisdiction
from drnalpha.sic_codes.models import Code


class Company(models.Model):
    name = models.CharField(max_length=255, db_index=True, blank=True, null=True)
    number = models.CharField(max_length=255, unique=True, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    jurisdictions = models.ManyToManyField(
        Jurisdiction,
        related_name="jurisdictions",
    )
    full_time_permanent_employees = models.PositiveIntegerField(
        "Full-time permanent employees", blank=True, null=True
    )
    full_time_contract_employees = models.PositiveIntegerField(
        "Full-time contract employees", blank=True, null=True
    )
    part_time_permanent_employees = models.PositiveIntegerField(
        "Part-time permanent employees", blank=True, null=True
    )
    part_time_contract_employees = models.PositiveIntegerField(
        "Part-time contract employees", blank=True, null=True
    )
    sic_codes = models.ManyToManyField(
        Code,
        related_name="company_sic_codes",
        verbose_name="SIC codes",
    )

    # Registered office address fields
    address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    locality = models.CharField(max_length=255, blank=True, null=True)
    po_box = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=255, blank=True, null=True)
    premises = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("number"),
        FieldPanel("jurisdictions", widget=CheckboxSelectMultiple),
        MultiFieldPanel(
            [
                FieldPanel("full_time_permanent_employees"),
                FieldPanel("full_time_contract_employees"),
                FieldPanel("part_time_permanent_employees"),
                FieldPanel("part_time_contract_employees"),
            ],
            heading="Employees",
            classname="collapsible",
        ),
        AutocompletePanel("sic_codes"),
        MultiFieldPanel(
            [
                FieldPanel("address_line_1"),
                FieldPanel("address_line_2"),
                FieldPanel("locality"),
                FieldPanel("region"),
                FieldPanel("postal_code"),
            ],
            heading="Address",
            classname="collapsible",
        ),
    ]

    autocomplete_search_field = "name"

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Companies"

    def __str__(self):
        if self.name:
            return self.name
        elif self.pk:
            return "Company {:d}".format(self.pk)
        return "Company"

    def autocomplete_label(self):
        return self.name

    def get_sic_codes(self):
        return self.sic_codes.all()
