from django.urls import path, re_path

from . import forms, views

app_name = "finder"

named_finder_forms = (
    # ("info", forms.InfoForm),
    ("locations", forms.LocationsForm),
    ("employees", forms.EmployeesForm),
    ("activities", forms.ActivitiesForm),
    ("review", forms.ReviewForm),
)

finder_wizard = views.FinderWizard.as_view(
    named_finder_forms,
    url_name="finder:step",
    done_step_name="done",
)

urlpatterns = [
    path("", views.index, name="index"),
    path("results/", views.results_list, name="results"),
    path("regulations/", views.regulation_list, name="regulation-index"),
    # path("regulations/<int:pk>/", views.regulation_detail, name="regulation-detail"),
    re_path(r"^(?P<step>.+)/$", finder_wizard, name="step"),
]
