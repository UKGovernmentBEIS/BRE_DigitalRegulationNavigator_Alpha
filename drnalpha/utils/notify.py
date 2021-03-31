from django.conf import settings

from notifications_python_client.notifications import NotificationsAPIClient


def send_notify_email(email_address, subject, message):
    api_key = getattr(settings, "NOTIFY_KEY", None)
    email_template_id = getattr(settings, "NOTIFY_EMAIL_TEMPLATE_ID", None)

    if not api_key and not email_template_id:
        return

    notifications_client = NotificationsAPIClient(api_key)
    response = notifications_client.send_email_notification(
        email_address=email_address,
        template_id=email_template_id,
        personalisation={
            "subject": subject,
            "message": message,
        },
    )

    return response["id"]
