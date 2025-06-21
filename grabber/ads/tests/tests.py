from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Ad
from django.core.exceptions import ValidationError

User = get_user_model()

class AdModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

    def test_create_ad(self):
        ad = Ad.objects.create(
            title='Test Title',
            description='This is a test description.',
            price=123.45,
            images=["/media/test1.jpg", "/media/test2.jpg"],
            status='pending',
            user=self.user
        )
        self.assertEqual(ad.title, 'Test Title')
        self.assertEqual(ad.status, 'pending')
        self.assertEqual(ad.user.email, 'test@example.com')
        self.assertIsNotNone(ad.created_at)

    def test_str_representation(self):
        ad = Ad.objects.create(
            title='My Ad',
            description='Desc',
            price=50,
            user=self.user
        )
        self.assertEqual(str(ad), 'My Ad')

    def test_default_status(self):
        ad = Ad.objects.create(
            title='No Status Ad',
            description='No status provided',
            price=10,
            user=self.user
        )
        self.assertEqual(ad.status, 'draft')

    def test_invalid_status(self):
        ad = Ad(
            title='Bad Status Ad',
            description='Desc',
            price=20,
            status='notavalidstatus',
            user=self.user
        )
        with self.assertRaises(ValidationError):
            ad.full_clean()  # вручну викликаємо повну валідацію моделі

    def test_missing_required_fields(self):
        ad = Ad(user=self.user)
        with self.assertRaises(ValidationError):
            ad.full_clean()
