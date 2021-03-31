from django.contrib import admin

from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    autocomplete_fields = ["jurisdictions", "sic_codes"]
    list_display = ["__str__"]
    ordering = ["name", "pk"]
    search_fields = ["name"]
    fieldsets = [
        [
            None,
            {
                "fields": ["name", "number", "jurisdictions", "sic_codes"],
            },
        ],
        [
            "Employees",
            {
                "classes": ["collapse"],
                "fields": [
                    "full_time_permanent_employees",
                    "full_time_contract_employees",
                    "part_time_permanent_employees",
                    "part_time_contract_employees",
                ],
            },
        ],
        [
            "Address",
            {
                "classes": ["collapse"],
                "fields": [
                    "address_line_1",
                    "address_line_2",
                    "locality",
                    "region",
                    "postal_code",
                ],
            },
        ],
    ]
