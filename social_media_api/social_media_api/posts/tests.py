from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from posts.models import Post, Like
from notifications.models import Notification

User = get_user_model()

class LikeTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Create users
        self.user1 = User.objects.create_user(username='user1', password='pass1234')
        self.user2 = User.objects.create_user(username='user2', password='pass1234')
        
        # Create a post
        self.post = Post.objects.create(
            author=self.user2,
            title='Test Post',
            content='Test Content'
        )
        
        # Authenticate user1
        self.client.force_authenticate(user=self.user1)

    def test_like_post(self):
        """Test liking a post"""
        url = reverse('post-like', args=[self.post.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Like.objects.filter(user=self.user1, post=self.post).exists())
        
        # Check notification was created
        self.assertTrue(
            Notification.objects.filter(
                recipient=self.user2,
                actor=self.user1,
                verb='liked'
            ).exists()
        )

    def test_unlike_post(self):
        """Test unliking a post"""
        # First like the post
        Like.objects.create(user=self.user1, post=self.post)
        
        url = reverse('post-unlike', args=[self.post.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Like.objects.filter(user=self.user1, post=self.post).exists())

    def test_duplicate_like(self):
        """Test attempting to like a post twice"""
        Like.objects.create(user=self.user1, post=self.post)
        
        url = reverse('post-like', args=[self.post.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class NotificationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Create users
        self.user1 = User.objects.create_user(username='user1', password='pass1234')
        self.user2 = User.objects.create_user(username='user2', password='pass1234')
        
        # Authenticate user1
        self.client.force_authenticate(user=self.user1)

    def test_list_notifications(self):
        """Test retrieving user's notifications"""
        # Create a notification
        Notification.objects.create(
            recipient=self.user1,
            actor=self.user2,
            verb='followed'
        )
        
        url = reverse('notification-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_mark_notification_as_read(self):
        """Test marking a notification as read"""
        notification = Notification.objects.create(
            recipient=self.user1,
            actor=self.user2,
            verb='followed'
        )
        
        url = reverse('notification-mark-as-read', args=[notification.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)
