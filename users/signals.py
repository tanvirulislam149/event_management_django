from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator 
from django.core.mail import send_mail
from decouple import config


@receiver(post_save, sender=User)
def send_activation_mail(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_link = f"{config("FRONTEND_URL")}/users/activate/{instance.id}/{token}"
        message = f"Please activate your account by clicking this link - {activation_link}"
        
        try:
            send_mail(
                "Activation Link for Event Management",
                message,
                config("EMAIL_HOST_USER"),
                [instance.email],
                fail_silently=False,
            )
        except Exception:
            print("Error in sending email.")