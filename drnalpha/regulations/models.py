from django.db import models
from django.db.models.functions import FirstValue
from django.forms.widgets import CheckboxSelectMultiple

from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.search import index

from wagtailautocomplete.edit_handlers import AutocompletePanel

from drnalpha.sic_codes.models import Code


class Regulator(index.Indexed, models.Model):
    name = models.CharField("Short name", max_length=50, db_index=True)
    verbose_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    url = models.URLField("URL")
    description = RichTextField(blank=True)
    sic_codes = models.ManyToManyField(
        Code, related_name="regulator_sic_codes", verbose_name="SIC codes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("verbose_name"),
        FieldPanel("slug"),
        FieldPanel("url"),
        FieldPanel("description"),
        AutocompletePanel("sic_codes"),
    ]

    search_fields = [
        index.SearchField("name", boost=10),
        index.SearchField("verbose_name", partial_match=True, boost=10),
        index.SearchField("description"),
    ]

    autocomplete_search_field = "name"

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.verbose_name if self.verbose_name else self.name

    def autocomplete_label(self):
        return self.name


class Jurisdiction(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    autocomplete_search_field = "name"

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def autocomplete_label(self):
        return self.name


class CategoryQuerySet(models.QuerySet):
    def with_regulations_count(self):
        regulations_count = models.Window(
            expression=models.Count(models.F("regulations__id")),
            partition_by=models.F("name"),
        )
        return self.annotate(regulations_count=regulations_count)

    def with_example_regulation_name(self):
        example_regulation_name = models.Window(
            expression=FirstValue(models.F("regulations__name")),
            partition_by=models.F("name"),
            order_by=models.F("regulations__name").asc(),
        )
        return self.annotate(example_regulation_name=example_regulation_name)


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True)
    verbose_name = models.CharField(max_length=255, blank=True)
    description = RichTextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CategoryQuerySet.as_manager()

    autocomplete_search_field = "name"

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def autocomplete_label(self):
        return self.name


class Importance(models.IntegerChoices):
    MANDATORY = 0, "Mandatory"
    BEST_PRACTICE = 1, "Best practice"
    OPTIONAL = 2, "Optional"


class RegulationQuerySet(models.QuerySet):
    def for_jurisdictions(self, jurisdictions):
        return self.filter(jurisdictions__in=jurisdictions)

    def for_sic_codes(self, sic_codes):
        return self.filter(sic_codes__in=sic_codes)

    def group_by_category(self):
        return (
            Category.objects.filter(regulations__in=self)
            .with_regulations_count()
            .with_example_regulation_name()
            .order_by("name")
            .distinct("name")
        )

    def with_regulators(self):
        return self.prefetch_related("regulators")

    def with_jurisdictions(self):
        return self.prefetch_related("jurisdictions")


class Regulation(index.Indexed, ClusterableModel):
    name = models.CharField(max_length=255, db_index=True)
    description = RichTextField(blank=True)
    url = models.URLField("URL")
    regulators = models.ManyToManyField(
        Regulator,
        related_name="regulations",
        blank=True,
    )
    jurisdictions = models.ManyToManyField(
        Jurisdiction,
        related_name="regulations",
        blank=True,
    )
    is_blanket = models.BooleanField("is blanket?", db_index=True, default=False)
    importance = models.IntegerField(
        choices=Importance.choices, db_index=True, default=Importance.MANDATORY
    )
    sic_codes = models.ManyToManyField(
        Code, related_name="regulation_sic_codes", verbose_name="SIC codes"
    )
    categories = models.ManyToManyField(
        Category,
        related_name="regulations",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = RegulationQuerySet.as_manager()

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        FieldPanel("url"),
        FieldPanel("is_blanket"),
        FieldPanel("importance"),
        FieldPanel("jurisdictions", widget=CheckboxSelectMultiple),
        AutocompletePanel("regulators"),
        AutocompletePanel("sic_codes"),
        AutocompletePanel("categories"),
    ]

    search_fields = [
        index.SearchField("name", partial_match=True, boost=10),
        index.SearchField("description"),
    ]

    autocomplete_search_field = "name"

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def autocomplete_label(self):
        return self.name

    def get_regulators(self):
        return self.regulators.all()

    def get_regulator_names(self):
        return [regulator.name for regulator in self.regulators.all()]

    get_regulator_names.short_description = "Regulators"

    def get_jurisdictions(self):
        return self.jurisdictions.all()
