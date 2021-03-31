from django.urls import path

from drnalpha.companies.views import CompanySearchView, company_detail

app_name = "company"

urlpatterns = [
    path("search/", CompanySearchView.as_view(), name="search"),
    path("", company_detail, name="detail"),
]
