from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import DetailView, FormView

from wagtail.admin import messages

import requests

from drnalpha.companies.client import CompaniesHouseApiClient
from drnalpha.companies.forms import CompanySearchForm
from drnalpha.companies.models import Company
from drnalpha.tracker.decorators import tracker_required


class CompanySearchView(FormView):
    form_class = CompanySearchForm
    template_name = "patterns/pages/company_search.html"
    success_url = "company_search"

    def get(self, request, *args, **kwargs):
        if (
            request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
            or request.headers.get("x-requested-with") == "XMLHttpRequest"
        ):
            query = request.GET.get("company_name")
            data = self.search_companies(query)
            status_code = 200 if "error" not in data else requests.codes.bad_gateway
            return JsonResponse(data, status=status_code)

        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request, *args, **kwargs):
        print("xx")
        form = self.form_class(data=request.POST)
        data = {}
        if form.is_valid():
            name = form.cleaned_data["company_name"]
            number = form.cleaned_data["company_number"]

            try:
                client = CompaniesHouseApiClient()

                if number:
                    data = client.get_company_details(number)
                else:
                    results = client.search_companies(name)
                    data = [
                        {
                            "title": item["title"],
                            "company_number": item["company_number"],
                            "address": item["address"],
                        }
                        for item in results["items"]
                    ]

            except Exception as e:
                messages.error(
                    self.request,
                    "Exception: {}".format(e),
                )

        return render(
            request, self.template_name, self.get_context_data(form=form, data=data)
        )

    def search_companies(self, query):
        data = {}
        try:
            client = CompaniesHouseApiClient()
            results = client.search_companies(query)
            data["results"] = [
                {
                    "title": item["title"],
                    "company_number": item["company_number"],
                    "address": item["address"],
                }
                for item in results["items"]
            ]

        except Exception as e:
            data["error"] = ("Exception: {}".format(e),)

        return data


class CompanyDetail(DetailView):
    model = Company
    template_name = "patterns/pages/companies/company_detail.html"


@login_required()
@tracker_required()
def company_detail(request, tracker):
    return render(
        request,
        "patterns/pages/companies/company_detail.html",
        {
            "company": tracker.company,
        },
    )
