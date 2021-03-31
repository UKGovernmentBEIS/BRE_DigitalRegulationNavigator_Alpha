from urllib.parse import urljoin, urlparse

from django.contrib import messages
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.utils.http import url_has_allowed_host_and_scheme

from sesame.utils import get_query_string

from drnalpha.users.forms import LoginForm
from drnalpha.utils.notify import send_notify_email


def login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            send_login_email(request, user=form.get_user())

            messages.success(
                request,
                "We have sent you a sign in link. Please follow the link in the email to sign in.",
            )
            return redirect("/")
    else:
        form = LoginForm()

    return TemplateResponse(
        request,
        "patterns/pages/users/login.html",
        {
            "next": get_redirect_url(request),
            "form": form,
        },
    )


def send_login_email(request, *, user):
    context = {
        "user": user,
        "login_url": get_login_url(request, user=user),
    }

    subject = render_to_string(
        template_name="patterns/pages/users/login_email_subject.txt",
        context=context,
        request=request,
    )
    # Force subject to a single line to avoid header-injection
    # issues.
    subject = "".join(subject.splitlines())

    message = render_to_string(
        template_name="patterns/pages/users/login_email_body.txt",
        context=context,
        request=request,
    )

    if not send_notify_email(user.email, subject, message):
        html_message = render_to_string(
            template_name="patterns/pages/users/login_email_body.html",
            context=context,
            request=request,
        )
        user.email_user(subject, message, html_message=html_message)


def get_redirect_url(request):
    redirect_to = request.POST.get("next", request.GET.get("next", ""))
    redirect_to = remove_query_string(redirect_to)

    url_is_safe = url_has_allowed_host_and_scheme(
        url=redirect_to,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    )

    return redirect_to if url_is_safe else ""


def get_login_url(request, *, user):
    return (
        request.build_absolute_uri("/")[:-1]
        + get_redirect_url(request)
        + get_query_string(user)
    )


def remove_query_string(url):
    return urljoin(url, urlparse(url).path)
