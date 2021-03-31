from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from .models import Code


class CodeAdmin(ModelAdmin):
    model = Code
    list_display = ["code", "title"]
    menu_icon = "tag"
    ordering = ["code"]
    search_fields = ["code", "title"]


class CodeAdminGroup(ModelAdminGroup):
    menu_label = "SIC Codes"
    menu_icon = "tag"
    menu_order = 510
    items = [CodeAdmin]


modeladmin_register(CodeAdminGroup)
