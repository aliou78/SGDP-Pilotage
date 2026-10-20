from django.contrib.auth import authenticate
from django.test import TestCase
from django.urls import reverse

from .forms import UserUpdateForm
from .models import User


class UserActivationTests(TestCase):
	def setUp(self):
		self.admin = User.objects.create_user(
			username='admin',
			password='password123',
			role='admin',
		)
		self.agent = User.objects.create_user(
			username='agent',
			password='password123',
			role='agent',
		)

	def test_actif_controls_django_authentication(self):
		self.agent.actif = False
		self.agent.save()

		self.assertFalse(self.agent.is_active)
		self.assertIsNone(
			authenticate(username='agent', password='password123')
		)

	def test_activation_requires_post(self):
		self.client.force_login(self.admin)
		url = reverse('user_toggle_active', kwargs={'user_id': self.agent.id})

		response = self.client.get(url)

		self.assertEqual(response.status_code, 405)
		self.agent.refresh_from_db()
		self.assertTrue(self.agent.actif)

	def test_activation_post_toggles_account(self):
		self.client.force_login(self.admin)
		url = reverse('user_toggle_active', kwargs={'user_id': self.agent.id})

		response = self.client.post(url)

		self.assertRedirects(response, reverse('user_list'))
		self.agent.refresh_from_db()
		self.assertFalse(self.agent.actif)
		self.assertFalse(self.agent.is_active)

	def test_user_list_displays_consultation_role(self):
		consultation = User.objects.create_user(
			username='consultation',
			password='password123',
			role='consultation',
		)
		self.client.force_login(self.admin)

		response = self.client.get(reverse('user_list'))

		self.assertContains(response, 'Consultation')


class UserUpdatePasswordTests(TestCase):

	def setUp(self):
		self.user = User.objects.create_user(
			username='user_to_update',
			password='original-password',
			role='agent',
		)

	def update_form(self, password):
		return UserUpdateForm(
			data={
				'username': self.user.username,
				'first_name': self.user.first_name,
				'last_name': self.user.last_name,
				'password': password,
				'role': self.user.role,
				'telephone': self.user.telephone,
				'adresse': self.user.adresse,
				'actif': 'on',
			},
			instance=self.user,
		)

	def test_blank_password_retains_existing_hash(self):
		password_hash = self.user.password
		form = self.update_form('')

		self.assertTrue(form.is_valid(), form.errors)
		form.save()

		self.user.refresh_from_db()
		self.assertEqual(self.user.password, password_hash)
		self.assertTrue(self.user.check_password('original-password'))

	def test_nonblank_password_replaces_existing_password(self):
		form = self.update_form('replacement-password')

		self.assertTrue(form.is_valid(), form.errors)
		form.save()

		self.user.refresh_from_db()
		self.assertNotEqual(self.user.password, 'replacement-password')
		self.assertFalse(self.user.check_password('original-password'))
		self.assertTrue(self.user.check_password('replacement-password'))
