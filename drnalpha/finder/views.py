from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from formtools.wizard.views import NamedUrlSessionWizardView

from drnalpha.regulations.models import Regulation
from drnalpha.tracker.decorators import no_tracker_required

from .decorators import FINDER_DATA_KEY, finder_data_required
from .forms import RegulationFilterForm, RegulationFinderForm


@no_tracker_required
def index(request):
    return TemplateResponse(
        request,
        "patterns/pages/finder/index.html",
    )


class FinderWizard(NamedUrlSessionWizardView):
    TEMPLATES = {
        "activities": "activities_form",
        "review": "review_form",
    }

    def get_template_names(self):
        template_name = self.TEMPLATES.get(self.steps.current, "wizard_form")
        return f"patterns/pages/finder/{template_name}.html"

    def get_form_initial(self, step):
        if self.request.session.get(FINDER_DATA_KEY):
            return self.request.session[FINDER_DATA_KEY].get(step, {})
        return self.initial_dict.get(step, {})

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        # Make all form data so far submitted available to the review form template.
        # The review ("Check your answers") page is a form step itself so we can
        # easily go back to a previous step.
        if self.steps.current == "review":
            context.update({"finder_data": self.get_all_cleaned_data()})
        return context

    def render_goto_step(self, goto_step, **kwargs):
        self.storage.extra_data["next_step"] = (
            "review" if self.steps.current == "review" else None
        )
        return super().render_goto_step(goto_step, **kwargs)

    def get_next_step(self, step=None):
        next_step = self.storage.extra_data.get("next_step")
        if next_step:
            return next_step
        return super().get_next_step(step)

    def done(self, form_list, form_dict, **kwargs):
        # See: FinderForm clean()
        dumped_data = {step: form.dumped_data for step, form in form_dict.items()}
        self.request.session[FINDER_DATA_KEY] = dumped_data
        return redirect("finder:results")


@no_tracker_required
@finder_data_required
def results_list(request, finder_data):
    # Using a form means we don't need to manually convert the activities etc. back
    # into QuerySets.
    regulation_finder_form = RegulationFinderForm.for_finder_data(finder_data)

    if not regulation_finder_form.is_valid():
        redirect("finder:index")

    regulations = regulation_finder_form.get_filtered_queryset()
    categories = regulations.group_by_category()

    return TemplateResponse(
        request,
        "patterns/pages/finder/results_list.html",
        {
            "finder_data": regulation_finder_form.cleaned_data,
            "regulations_count": regulations.count(),
            "categories": categories,
            "categories_count": categories.count(),
        },
    )


@no_tracker_required
@finder_data_required
def regulation_list(request, finder_data):
    regulation_finder_form = RegulationFinderForm.for_finder_data(finder_data)

    if not regulation_finder_form.is_valid():
        redirect("finder:index")

    regulations = (
        regulation_finder_form.get_filtered_queryset()
        .with_jurisdictions()
        .with_regulators()
    )

    data = request.GET if bool(request.GET) else None
    form = RegulationFilterForm(data, queryset=regulations)
    is_filtered = False

    if form.is_valid():
        is_filtered = True
        regulations = form.get_filtered_queryset()
        form = RegulationFilterForm(data, queryset=regulations)

    return TemplateResponse(
        request,
        "patterns/pages/finder/regulation_list.html",
        {
            "form": form,
            "is_filtered": is_filtered,
            "regulations": regulations,
            "regulations_count": regulations.count(),
        },
    )


def regulation_detail(request, pk):
    regulation = get_object_or_404(Regulation, pk=pk)

    return TemplateResponse(
        request,
        "patterns/pages/finder/regulation_detail.html",
        {
            "regulation": regulation,
        },
    )
