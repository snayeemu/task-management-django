from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from tasks.models import Tasks

def sent_email(sender, instance, action, **kwargs):
    if action == "post_add":
        emails = [emp.email for emp in instance.employees.all()]
        send_mail(
            "New Task Assigned",
            f"You have assigned to: {instance.title}",
            "snayeemu@gmail.com",
            emails,
            fail_silently=False,
        )


m2m_changed.connect(sent_email, sender=Tasks.employees.through)
