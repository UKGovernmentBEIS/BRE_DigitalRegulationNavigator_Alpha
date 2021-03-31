import debounce from '../utils/debounce';

class CompaniesHouseSearch {
    static selector() {
        return '[data-companies-house-input]';
    }

    constructor() {
        this.APIurl = `/company/search/?company_name=`;
        this.searchInput = document.querySelector(
            '[data-companies-house-input]',
        );
        this.searchResults = document.querySelector(
            '[data-companies-house-results]',
        );
        this.searchResultsWrapper = document.querySelector(
            '[data-companies-house-wrapper]',
        );

        this.manualCompanyNameInput = document.getElementById(
            'id_company_name',
        );

        this.hiddenField = document.getElementById('id_company_number');
        this.bindEvents();
    }

    populateSearchResults() {
        // Clear previous results on each new query
        this.searchResults.innerHTML = '';

        // Construct URL
        const url = `${this.APIurl}${this.searchInput.value}`;

        fetch(url, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.results.length) {
                    this.searchResults.style.display = 'block';

                    /* eslint-disable array-callback-return */
                    return data.results.map((result) => {
                        const wrapper = document.createElement('li');
                        wrapper.classList.add('companies-house__item-wrapper');

                        // Set company number
                        wrapper.setAttribute(
                            'data-companies-house-id',
                            result.company_number,
                        );

                        // Set result item content
                        wrapper.innerHTML = `
                            <div class="companies-house__item companies-house__item--title">${
                                result.title
                            }</div>
                            <div class="companies-house__item companies-house__item--number">${
                                result.company_number
                            }</div>
                            <div class="companies-house__item companies-house__item--address">
                                ${
                                    result.address.premises
                                        ? `${result.address.premises},`
                                        : ''
                                }
                                ${
                                    result.address.address_line_1
                                        ? `${result.address.address_line_1},`
                                        : ''
                                }
                                ${
                                    result.address.address_line_2
                                        ? `${result.address.address_line_2},`
                                        : ''
                                }
                                ${
                                    result.address.locality
                                        ? `${result.address.locality},`
                                        : ''
                                }
                                ${
                                    result.address.region
                                        ? `${result.address.region},`
                                        : ''
                                }
                                ${
                                    result.address.postal_code
                                        ? result.address.postal_code
                                        : ''
                                }
                            </div>
                        `;

                        // Append content to DOM
                        this.searchResults.appendChild(wrapper);
                    });
                }

                // If no results are returned from the API
                this.searchResults.innerHTML = `
                    <li class="companies-house__item-wrapper">
                        <div class="companies-house__item companies-house__item--no-results">
                            No matching company found.
                        </div>
                    </li>
                `;
                return false;
            })
            .catch((error) => {
                /* eslint-disable no-console */
                console.log(error);
            });
    }

    // Populate search input with clicked company
    populateInput(event) {
        if (event.target.classList.contains('companies-house__item')) {
            const title = event.target.parentNode.querySelector(
                '.companies-house__item--title',
            ).textContent;
            const companyID = event.target.parentNode.getAttribute(
                'data-companies-house-id',
            );

            // Set search input value to company name
            this.searchInput.value = title;

            // Set hidden input field to company ID
            this.hiddenField.value = companyID;

            // Hide results container
            this.searchResults.style.display = 'none';
        }
    }

    // Hide results when clicking away
    handleClickOutside(event) {
        const insideResults = this.searchResults.contains(event.target);
        const insideWrapper = this.searchResultsWrapper.contains(event.target);

        if (!insideResults && !insideWrapper) {
            this.searchResults.style.display = 'none';
        }
    }

    // Hide results when pressing escape key
    handleEscape(event) {
        if (event.key === 'Escape') {
            this.searchResults.style.display = 'none';
        }
    }

    bindEvents() {
        // If a previous search returned a company ID,
        // show previously searched for company name
        if (this.hiddenField.value.length) {
            this.searchInput.value = this.manualCompanyNameInput.value;
        }

        // Populate as user types
        this.searchInput.addEventListener(
            'keyup',
            debounce(() => {
                this.populateSearchResults();
                this.manualCompanyNameInput.value = this.searchInput.value;
            }, 200),
        );

        // Populate on Enter key and prevent form submission
        this.searchInput.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                event.preventDefault();
                this.populateSearchResults();
            }
        });

        this.searchResults.addEventListener('click', (event) => {
            this.populateInput(event);
        });

        document.body.addEventListener('mousedown', (event) => {
            this.handleClickOutside(event);
        });

        document.body.addEventListener('keydown', (event) => {
            this.handleEscape(event);
        });
    }
}

export default CompaniesHouseSearch;

export const initCompaniesHouseSearch = () => {
    const chSearches = [
        ...document.querySelectorAll('[data-companies-house-input]'),
    ];
    return chSearches.map((item) => new CompaniesHouseSearch(item));
};
