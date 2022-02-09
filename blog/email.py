from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse


def notify_followers_about_new_post(followers_profile, post):
    context = {
        "post": post,
        "post_url": reverse('post-detail', kwargs={'pk': post.id}),
    }

    email_body = render_to_string("blog/notify_followers_about_new_post.txt", context)

    email = EmailMessage(
        subject="New post from one of your followers",
        body=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[p.user.email for p in followers_profile]
    )

    return email.send(fail_silently=False)