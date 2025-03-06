from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

@receiver(post_save, sender=User)
def sent_confirmation_email(sender, instance, created, **kwargs):
    try:
        if created:
            subject = "Activate Your Tasks Management Account"
            token = default_token_generator.make_token(instance)
            url=f"{settings.FRONTEND_URL}/user/activate/{instance.id}/{token}"
            message = f"To activate you account go to the link below:\n\n{url}\n\nThank You"
            recipient_list = [instance.email]

            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
    except Exception as e:
        print(f"Failed to sent mail to {instance.email}: {str(e)}")

@receiver(post_save, sender=User)
def assign_role(sender, instance, created, **kwargs):
    if created:
        user_group, isCreated = Group.objects.get_or_create(name="User")
        instance.groups.add(user_group)
        instance.save()