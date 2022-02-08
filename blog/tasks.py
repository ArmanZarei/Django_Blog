from __future__ import absolute_import, unicode_literals
from celery import shared_task

from blog.models import Tag, Post
import random


@shared_task
def random_tag_post(post_id):
    post = Post.objects.get(id=post_id)

    tags = Tag.objects.all()
    sample_cnt = random.randint(1, len(tags))
    tags = tags.order_by('?')[:sample_cnt]

    post.tag_set.add(*tags)

    return f"Post \"{post.title}\" tagged!"
