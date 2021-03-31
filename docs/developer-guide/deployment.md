# DRN Alpha — hosts and deployment

The development container comes preinstalled with Fabric, Heroku CLI and AWS CLI. You must [install the GovPaaS CloudFoundry
CLI manually](https://github.com/cloudfoundry/cli/wiki/V7-CLI-Installation-Guide)

## Deployed environments

| Environment | Branch | URL                                                       | GovPaaS                   |
| ----------- | ------ | --------------------------------------------------------- | ------------------------- |
| Sandbox     | `main` | e.g. https://beis-bre-drn-alpha.london.cloudapps.digital/ | e.g. `beis-bre-drn-alpha` |

## Login to GovPaaS

Please log in to GovPaas before executing any commands for servers hosted there
using the `cf login -a api.london.cloud.service.gov.uk --sso` command.

Follow the [GovPaaS deployment documentation](https://docs.cloud.service.gov.uk/deploying_apps.html#deploy-a-django-app)
for deployment instructions

## Scheduled tasks

When you set up a server you should make sure the following scheduled tasks are set.

- `django-admin publish_scheduled_pages` - every 10 minutes or more often. This is necessary to make publishing scheduled pages work.
- `django-admin clearsessions` - once a day (not necessary, but useful).
- `django-admin update_index` - once a day (not necessary, but useful to make sure the search index stays intact).
