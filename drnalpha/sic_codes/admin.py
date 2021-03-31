from django.contrib import admin

from .models import Code


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ["code", "title"]
    search_fields = ["code", "title"]
