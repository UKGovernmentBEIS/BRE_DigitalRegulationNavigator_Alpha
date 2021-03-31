import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

import requests

from drnalpha.sic_codes.models import Code

logger = logging.getLogger(__name__)


class CompaniesHouseApiClient:
    base_url = "https://api.company-information.service.gov.uk"

    def __init__(self):
        """
        Ensure the API key is set before proceeding
        """
        self.api_key = getattr(settings, "COMPANIES_HOUSE_API_KEY")
        if not self.api_key:
            raise ImproperlyConfigured("Companies House API key not set")

    def get(self, endpoint, **data):
        """
        Wrapper for GET requests to Companies House API
        """

        response = requests.get(endpoint, params=data, auth=(self.api_key, ""))

        if response.ok:
            return response
        # HTTP 429 signifies we have been rate-limited
        elif response.status_code == requests.codes.too_many:
            logger.error(f"Hit rate limit on {endpoint}")
            response.raise_for_status()
        # Handle other HTTP errors
        else:
            logger.error(f"HTTP {response.status_code} error for {endpoint}")
            response.raise_for_status()

    def search_companies(self, search_string):
        """
        Search companies
        https://developer.company-information.service.gov.uk/api/docs/search/companies/companysearch.html
        """
        endpoint = f"{self.base_url}/search/companies"
        try:
            response = self.get(f"{endpoint}", q=search_string)
            return response.json()
        except ValueError as e:
            logger.exception(f"Could not decode results from {endpoint}")
            raise e
        except Exception as e:
            raise e

    def get_company(self, company_id):
        """
        companyProfile resource
        https://developer.company-information.service.gov.uk/api/docs/company/company_number/companyProfile-resource.html
        """
        endpoint = f"{self.base_url}/company"
        try:
            response = self.get(f"{endpoint}/{company_id}")
            return response.json()
        except ValueError as e:
            logger.exception(f"Could not decode results from {endpoint}")
            raise e
        except Exception as e:
            raise e

    def get_company_sic_codes(self, company_id):
        """
        Return the SIC Code objects corresponding to a given company_id
        """
        details = self.get_company(company_id)
        if details and "sic_codes" in details:
            sic_codes = []
            for sic_code in details["sic_codes"]:
                try:
                    sic_codes.append(Code.objects.get(code=sic_code))
                except Code.DoesNotExist:
                    logger.warning(
                        f"Could not find SIC Code corresponding to code value {sic_code}"
                    )
            return sic_codes

    def get_company_details(self, company_id):
        """
        Return a subset of the company information, with SIC Code lookup
        """
        if details := self.get_company(company_id):
            # Base details
            filtered_details = {
                "company_name": details["company_name"],
                "company_number": details["company_number"],
                "company_status": details["company_status"],
                "registered_office_address": details["registered_office_address"],
            }

            filtered_details["sic_codes"] = []
            if "sic_codes" in details:
                for sic_code in details["sic_codes"]:
                    try:
                        filtered_details["sic_codes"].append(
                            Code.objects.get(code=sic_code)
                        )
                    except Code.DoesNotExist:
                        logger.warning(
                            f"Could not find SIC Code corresponding to code value {sic_code}"
                        )

            return filtered_details
