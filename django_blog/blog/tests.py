from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

class AuthTests(TestCase):
    def test_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!',
        })
        self.assertEqual(response.status_code, 302)  # Redirect to profile
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_login(self):
        User.objects.create_user(username='testuser', email='testuser@example.com', password='Testpass123!')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'Testpass123!',
        })
        self.assertEqual(response.status_code, 302)  # Redirect to profile

    def test_logout(self):
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='Testpass123!')
        self.client.login(username='testuser', password='Testpass123!')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'logged out')

    def test_profile_view_and_update(self):
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='Testpass123!')
        self.client.login(username='testuser', password='Testpass123!')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('profile'), {
            'username': 'updateduser',
            'email': 'updated@example.com',
        })
        self.assertEqual(response.status_code, 302)  # Redirect to profile
        user.refresh_from_db()
        self.assertEqual(user.username, 'updateduser')
        self.assertEqual(user.email, 'updated@example.com')

class PostCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='author', password='pass123')
        self.other_user = User.objects.create_user(username='other', password='pass123')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)

    def test_post_list_view(self):
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_post_detail_view(self):
        response = self.client.get(reverse('post-detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Content')

    def test_create_post_authenticated(self):
        self.client.login(username='author', password='pass123')
        response = self.client.post(reverse('post-create'), {
            'title': 'New Post',
            'content': 'New Content',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='New Post').exists())

    def test_create_post_unauthenticated(self):
        response = self.client.post(reverse('post-create'), {
            'title': 'No Auth',
            'content': 'No Auth Content',
        })
        # Should redirect to login page
        self.assertRedirects(response, '/login/?next=/posts/new/')

    def test_edit_post_by_author(self):
        self.client.login(username='author', password='pass123')
        response = self.client.post(reverse('post-edit', args=[self.post.pk]), {
            'title': 'Edited Title',
            'content': 'Edited Content',
        })
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Edited Title')

    def test_edit_post_by_other_user(self):
        self.client.login(username='other', password='pass123')
        response = self.client.post(reverse('post-edit', args=[self.post.pk]), {
            'title': 'Hacked Title',
            'content': 'Hacked Content',
        })
        self.assertNotEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertNotEqual(self.post.title, 'Hacked Title')

    def test_delete_post_by_author(self):
        self.client.login(username='author', password='pass123')
        response = self.client.post(reverse('post-delete', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_delete_post_by_other_user(self):
        self.client.login(username='other', password='pass123')
        response = self.client.post(reverse('post-delete', args=[self.post.pk]))
        self.assertNotEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())
