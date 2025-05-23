from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from follows.models import Follow

User = get_user_model()

class TestFollowsViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.follower = User.objects.create_user(
            email='follower@example.com',
            username='follower',
            password='pass'
        )
        self.followed = User.objects.create_user(
            email='followed@example.com',
            username='followed',
            password='pass'
        )
        self.other_user = User.objects.create_user(
            email='other@example.com',
            username='other',
            password='pass'
        )
        self.client.force_authenticate(user=self.follower)

    def test_create_follow(self):
        url = '/api/follows/follows/'
        data = {'followed': self.followed.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Follow.objects.filter(
            follower=self.follower,
            followed=self.followed
        ).exists())

    def test_cannot_follow_self(self):
        url = '/api/follows/follows/'
        data = {'followed': self.follower.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Follow.objects.filter(
            follower=self.follower,
            followed=self.follower
        ).exists())

    def test_cannot_follow_twice(self):
        Follow.objects.create(follower=self.follower, followed=self.followed)
        url = '/api/follows/follows/'
        data = {'followed': self.followed.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Follow.objects.filter(
            follower=self.follower,
            followed=self.followed
        ).count(), 1)

    def test_list_follows(self):
        Follow.objects.create(follower=self.follower, followed=self.followed)
        Follow.objects.create(follower=self.follower, followed=self.other_user)
        url = '/api/follows/follows/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_following_endpoint(self):
        Follow.objects.create(follower=self.follower, followed=self.followed)
        Follow.objects.create(follower=self.follower, followed=self.other_user)
        url = '/api/follows/follows/following/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['followed']['username'], self.followed.username)
        self.assertEqual(response.data[1]['followed']['username'], self.other_user.username)

    def test_followers_endpoint(self):
        Follow.objects.create(follower=self.followed, followed=self.follower)
        Follow.objects.create(follower=self.other_user, followed=self.follower)
        url = '/api/follows/follows/followers/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['follower']['username'], self.followed.username)
        self.assertEqual(response.data[1]['follower']['username'], self.other_user.username)

    def test_unauthenticated_access(self):
        self.client.force_authenticate(user=None)
        url = '/api/follows/follows/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_follow(self):
        follow = Follow.objects.create(follower=self.follower, followed=self.followed)
        url = f'/api/follows/follows/{follow.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Follow.objects.filter(id=follow.id).exists())

    def test_cannot_delete_others_follow(self):
        follow = Follow.objects.create(follower=self.other_user, followed=self.followed)
        url = f'/api/follows/follows/{follow.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Follow.objects.filter(id=follow.id).exists()) 