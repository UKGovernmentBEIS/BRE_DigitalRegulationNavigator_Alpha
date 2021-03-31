from django import forms


class CompanySearchForm(forms.Form):
    company_name = forms.CharField(label="Company name", required=False)
    company_number = forms.CharField(
        label="Company number", required=False, widget=forms.HiddenInput
    )
