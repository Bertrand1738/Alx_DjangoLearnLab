from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

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
