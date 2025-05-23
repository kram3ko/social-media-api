from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from follows.models import Follow
from follows.serializers import FollowCreateSerializer, FollowSerializer

User = get_user_model()

class TestFollowCreateSerializer(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
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
        self.request = self.factory.get('/')
        self.request.user = self.follower

    def test_cannot_follow_self(self):
        data = {'followed': self.follower.id}
        serializer = FollowCreateSerializer(data=data, context={'request': self.request})
        serializer.is_valid()
        self.assertIn('non_field_errors', serializer.errors)
        self.assertTrue(
            any('cant follow yourself' in error.lower()
                for error in serializer.errors['non_field_errors'])
        )

    def test_cannot_follow_same_user_twice(self):
        Follow.objects.create(follower=self.follower, followed=self.followed)
        data = {'followed': self.followed.id}
        serializer = FollowCreateSerializer(data=data, context={'request': self.request})
        serializer.is_valid()
        self.assertIn('non_field_errors', serializer.errors)
        self.assertTrue(
            any('already following' in error.lower()
                for error in serializer.errors['non_field_errors'])
        )

    def test_successful_follow(self):
        data = {'followed': self.followed.id}
        serializer = FollowCreateSerializer(data=data, context={'request': self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data['followed'], self.followed)

    def test_missing_followed_field(self):
        data = {}
        serializer = FollowCreateSerializer(data=data, context={'request': self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('followed', serializer.errors)


class TestFollowSerializer(TestCase):
    def setUp(self):
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
        self.follow = Follow.objects.create(
            follower=self.follower,
            followed=self.followed
        )

    def test_serializer_fields(self):
        serializer = FollowSerializer(self.follow)
        data = serializer.data
        
        self.assertIn('follower', data)
        self.assertIn('followed', data)
        self.assertIn('liked_at', data)
        
        # Check nested user data
        self.assertIn('username', data['follower'])
        self.assertIn('email', data['follower'])
        self.assertIn('username', data['followed'])
        self.assertIn('email', data['followed'])