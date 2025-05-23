from django.test import TestCase
from django.contrib.auth import get_user_model
from posts.models import Post, Like, Comment
from posts.serializers import PostSerializer, PostCreateSerializer, LikeSerializer, CommentSerializer
from rest_framework.exceptions import ValidationError
from datetime import datetime
from django.utils import timezone

User = get_user_model()

class PostSerializersTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@example.com', username='user', password='pass')
        self.post = Post.objects.create(user=self.user, post='Test post')

    def test_post_serializer_output(self):
        serializer = PostSerializer(self.post)
        data = serializer.data
        self.assertEqual(data['post'], 'Test post')
        self.assertEqual(data['user']['username'], 'user')

    def test_post_create_serializer_valid(self):
        data = {'post': 'New post'}
        serializer = PostCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_post_create_serializer_invalid(self):
        data = {'post': ''}
        serializer = PostCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())  # blank allowed

    def test_like_serializer_output(self):
        like = Like.objects.create(user=self.user, post=self.post)
        serializer = LikeSerializer(like)
        data = serializer.data
        self.assertEqual(data['post']['post'], 'Test post')
        self.assertEqual(data['user'], self.user.id)

    def test_comment_serializer_output(self):
        comment = Comment.objects.create(user=self.user, post=self.post, comment='Nice!')
        serializer = CommentSerializer(comment)
        data = serializer.data
        self.assertEqual(data['comment'], 'Nice!')
        self.assertEqual(data['user']['username'], 'user')
        self.assertEqual(data['post']['post'], 'Test post') 