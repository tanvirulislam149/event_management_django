from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from events.models import Event
from django.core.mail import send_mail
from decouple import config

@receiver(m2m_changed, sender=Event.participants.through)
def event_confirm_mail(sender, instance, **kwargs):
    print("signal save")
    user_emails = [user.email for user in instance.participants.all()]
    print(user_emails, instance.participants.all())
    activation_link = f"{config("FRONTEND_URL")}/events/accept_invitation/{instance.id}/"
    message = f"Please accept the invitation for {instance.name}. Click the link to accept invitation - {activation_link}"
    
    try:
        send_mail(
            "Accept the invitation for Event Management",
            message,
            config("EMAIL_HOST_USER"),
            user_emails,
            fail_silently=False,
        )
    except Exception:
        print("Error in sending email.")
