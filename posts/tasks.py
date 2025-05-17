from celery import shared_task
from django.utils import timezone

from posts.models import Post
import requests


def get_random_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    request = requests.get(url)
    if request.status_code == 200:
        joke = request.json()
        return f"{joke['setup']} {joke['punchline']}"
    return "Didn't get any joke."


@shared_task
def publish_schedule_post(post_id):
    try:
        post = Post.objects.get(id=post_id, published=False)
        post.published = True
        post.published_at = post.schedule_date
        post.save()
        print(f"Post {post_id} published!")
    except Post.DoesNotExist:
        print(f"Post {post_id} does not exist or already published!")
    except Exception as e:
        print(f"Failed to publish post {post_id}: {e}")


@shared_task
def make_posts_public():
    try:

        @shared_task
        def make_posts_public():
            try:
                post = Post.objects.create(
                    user_id=1,
                    post=get_random_joke(),
                    published_at=timezone.now(),
                )
                post.save()
            except Exception as e:
                print(f"Failed to create post: {e}")
    except Exception as e:
        print(f"Failed to create post: {e}")
