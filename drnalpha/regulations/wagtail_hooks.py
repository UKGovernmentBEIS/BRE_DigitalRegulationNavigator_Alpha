from django.templatetags.static import static
from django.utils.html import format_html

from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from wagtail.core import hooks

from .models import Category, Jurisdiction, Regulation, Regulator


@hooks.register("insert_editor_css", order=1)
def editor_css():
    return format_html(
        '<link rel="stylesheet" href="{}">', static("css/wagtailautocomplete.css")
    )


class RegulatorAdmin(ModelAdmin):
    model = Regulator
    list_display = ["name", "verbose_name"]
    menu_icon = "group"
    ordering = ["name"]
    search_fields = ["name", "verbose_name"]


class RegulationAdmin(ModelAdmin):
    model = Regulation
    list_display = ["name", "get_regulator_names"]
    menu_icon = "doc-full-inverse"
    ordering = ["name"]
    search_fields = ["name"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.with_regulators()


class JurisdictionAdmin(ModelAdmin):
    model = Jurisdiction
    list_display = ["name"]
    menu_icon = "tag"
    menu_label = "Jurisdictions"
    ordering = ["name"]
    search_fields = ["name"]


class CategoryAdmin(ModelAdmin):
    model = Category
    list_display = ["name", "verbose_name"]
    menu_icon = "tag"
    ordering = ["name"]
    search_fields = ["name", "verbose_name"]


class RegulationsAdminGroup(ModelAdminGroup):
    menu_label = "Regulations"
    menu_icon = "clipboard-list"
    menu_order = 511
    items = [RegulatorAdmin, RegulationAdmin, JurisdictionAdmin, CategoryAdmin]


modeladmin_register(RegulationsAdminGroup)
