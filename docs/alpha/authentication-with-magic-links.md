# Authentication with “Magic Links”

## What was in Discovery?

Page 92 - Step 2

> Self Assessment: A user can start a new tracker page based on provided business information. A hash gets generated for the tracker page. The user gets a unique URL to revisit, or can enter the hash on the start page to retrieve their tracker. This way registration and login functionality is not yet required.

## What did we do instead and why?

We looked at implementing a unique URL for each Tracker using a UUID. As the URL’s could easily be shared copied we decided to look at some form of log in to protect the user’s information.

We wanted something simpler than traditional username and passwords such as Slack's "magic "links". They offer a simple sign in system you enter your email address and they send a unique sign in link that once clicked signs the user in without the need to enter a password. The “magic link” contains a specially crafted token which can only be used for a short time.

Although a visitor only needs a valid sign in link to access the service, the relatively short time the link is valid for reduces the risk that someone other than the intended recipient of the link can sign in.

We looked around for existing implementations for Django rather than creating our own and settled on the open-source library, [Django Sesame](https://github.com/aaugustin/django-sesame) as it has comprehensive documentation and at the time of writing, no open issues on Github.

Each time a user wishes to log in, they enter their email address and are sent a new, short-lived log in link, such as:

    https://example.com/accounts/login/?token=AAAAAQJE_-GvdStixvsaAD1x

This expires after a set time and can be configured in seconds with the SESAME_MAX_AGE setting, e.g. `SESAME_MAX_AGE = 60 * 5`.

You can also change the name of token as it appears in the log in URL with `SESAME_TOKEN_NAME` and the length of the token itself with `SESAME_SIGNATURE_SIZE`. See [Generating URLs](https://github.com/aaugustin/django-sesame#generating-urls) and [Token Security](https://github.com/aaugustin/django-sesame#tokens-security).

## Key points:

- Uses Django’s built in authentication and permissions system
- User account information is minimal with email address the only personally identifiable info
- Only signed in users can access their previously saved information
- Can be integrated with additional authentication methods (single-sign on, 2-FA…)

## Links:

- https://www.okta.com/blog/2020/09/magic-links/
