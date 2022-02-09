from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.contrib.auth.models import User
from celery.utils.log import get_task_logger
from blog.models import Tag, Post
import random
from .email import notify_followers_about_new_post


logger = get_task_logger(__name__)


@shared_task
def random_tag_post(post_id):
    post = Post.objects.get(id=post_id)

    tags = Tag.objects.all()
    sample_cnt = random.randint(1, len(tags))
    tags = tags.order_by('?')[:sample_cnt]

    post.tag_set.add(*tags)

    return f"Post \"{post.title}\" tagged!"


@shared_task
def send_email_to_followers(user_id, post_id):
    user = User.objects.get(pk=user_id)
    post = Post.objects.get(pk=post_id)

    logger.info(f"Notified followers about post {post.title}")

    return notify_followers_about_new_post(user.profile.followers.all(), post)
