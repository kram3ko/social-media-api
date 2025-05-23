from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from posts.models import Post, Like, Comment

User = get_user_model()

class PostViewsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@example.com', username='user', password='pass')
        self.other = User.objects.create_user(email='other@example.com', username='other', password='pass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(user=self.user, post='Test post')

    def test_post_list(self):
        url = reverse('posts:posts-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(p['post'] == 'Test post' for p in response.data))

    def test_post_create(self):
        url = reverse('posts:create-post')
        data = {'post': 'Created post'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.filter(post='Created post').count(), 1)

    def test_like_post(self):
        url = reverse('posts:like-post', args=[self.post.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Like.objects.filter(user=self.user, post=self.post).count(), 1)

    def test_unlike_post(self):
        Like.objects.create(user=self.user, post=self.post)
        url = reverse('posts:like-post', args=[self.post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.filter(user=self.user, post=self.post).count(), 0)

    def test_create_comment(self):
        url = reverse('posts:post-comments', args=[self.post.id])
        data = {'comment': 'New comment'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.filter(post=self.post, comment='New comment').count(), 1) 