import logging

import requests
from celery import shared_task
from django.db import transaction
from django.utils import timezone

from posts.models import Post

logger = logging.getLogger(__name__)


def get_random_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    logger.info(f"Fetching random joke from {url}")
    request = requests.get(url)
    if request.status_code == 200:
        joke = request.json()
        return f"{joke['setup']} {joke['punchline']}"
    return None


@shared_task
def publish_schedule_post(post_id):
    try:
        post = Post.objects.get(id=post_id, published=False)
        post.published = True
        post.published_at = post.schedule_date
        post.save()
        logger.info(f"Post {post_id} published successfully.")
    except Post.DoesNotExist:
        logger.warning(f"Post {post_id} does not exist or is already published.")
    except Exception as e:
        logger.error(f"Error publishing post {post_id}: {e}")


@shared_task
def make_posts_public():
    joke = get_random_joke()
    if joke:
        with transaction.atomic():
            post = Post.objects.create(
                user_id=1,
                post=joke,
                published_at=timezone.now(),
            )
            post.save()
            logger.info(f"Post created with ID: {post.id}")