import '@babel/polyfill';
import { initAll } from 'govuk-frontend';
import { initAccordion } from './components/accordion';
import { initCompaniesHouseSearch } from './components/companies-house';

import '../sass/main.scss';

document.addEventListener('DOMContentLoaded', () => {
    // Worth us only initialising the specific components we use further down the line, but for the sake of speed in Alpha:
    initAll();

    initAccordion();
    initCompaniesHouseSearch();
});
