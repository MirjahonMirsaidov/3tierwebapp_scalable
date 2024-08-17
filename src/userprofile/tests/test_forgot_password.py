from rest_framework.test import APITestCase

from userprofile.models import UserProfile, Role


class TestProfileInfo(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserProfile.objects.create_user(
            email='ichigoat@mail.com', password='password', phone_number='935684513',
            role=Role.objects.get(name='superadmin'), first_name='Ichigo', last_name='Kurosaki',
            middle_name='Ataraxia',
        )

        cls.post_data = {'email': 'ichigoat@mail.com', 'password': 'new_password'}

        cls.read_url = '/api/v1/profile/forgot-password/'
        cls.reset_url = '/api/v1/profile/reset-password/'

    def test_forgot_password(self):
        response = self.client.post(self.read_url, data=self.post_data, format='json')

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 201)
        self.assertFalse(self.user.check_password('password'))
        self.assertTrue(self.user.check_password('new_password'))

    def test_reset_password(self):
        self.client.force_authenticate(user=self.user)
        content = {'old_password': 'password', 'new_password': 'new_password'}
        response = self.client.post(self.reset_url, data=content, format='json')

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 201)
        self.assertFalse(self.user.check_password('password'))
        self.assertTrue(self.user.check_password('new_password'))

    def test_reset_password_wrong_old_password(self):
        self.client.force_authenticate(user=self.user)
        content = {'old_password': 'wrong_password', 'new_password': 'new_password'}
        response = self.client.post(self.reset_url, data=content, format='json')

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertTrue(self.user.check_password('password'))
        self.assertFalse(self.user.check_password('new_password'))








