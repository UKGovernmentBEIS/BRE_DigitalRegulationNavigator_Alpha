from django.contrib import admin

from .models import Category, Jurisdiction, Regulation, Regulator


@admin.register(Regulator)
class RegulatorAdmin(admin.ModelAdmin):
    autocomplete_fields = ["sic_codes"]
    list_display = ["name", "verbose_name"]
    search_fields = ["name", "verbose_name"]


@admin.register(Jurisdiction)
class JurisdictionAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "verbose_name"]
    search_fields = ["name", "verbose_name"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Regulation)
class RegulationAdmin(admin.ModelAdmin):
    autocomplete_fields = ["regulators", "jurisdictions", "sic_codes", "categories"]
    list_display = ["name", "get_regulator_names"]
    list_filter = ["jurisdictions", "categories"]
    radio_fields = {"importance": admin.VERTICAL}
    search_fields = ["name"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.with_regulators()
