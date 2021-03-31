from django.db import models


class CodeQuerySet(models.QuerySet):
    def related_to_food(self):
        return self.filter(
            models.Q(code__startswith="10")
            | models.Q(code__startswith="11")
            | models.Q(code__startswith="56")
        )


class Code(models.Model):
    code = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=255, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CodeQuerySet.as_manager()

    autocomplete_search_field = "title"

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code}: {self.title}"

    def autocomplete_label(self):
        return str(self)
