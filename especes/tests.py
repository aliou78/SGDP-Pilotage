from django.test import TestCase
from django.urls import reverse

from accounts.models import User

from .models import Espece


class EspeceActivationTests(TestCase):
	def setUp(self):
		self.admin = User.objects.create_user(
			username='admin',
			password='password123',
			role='admin',
		)
		self.espece = Espece.objects.create(nom='Espece test')

	def test_activation_requires_post(self):
		self.client.force_login(self.admin)
		url = reverse('espece_toggle_active', kwargs={'pk': self.espece.id})

		response = self.client.get(url)

		self.assertEqual(response.status_code, 405)

	def test_activation_post_preserves_species(self):
		self.client.force_login(self.admin)
		url = reverse('espece_toggle_active', kwargs={'pk': self.espece.id})

		response = self.client.post(url)

		self.assertRedirects(response, reverse('espece_list'))
		self.espece.refresh_from_db()
		self.assertFalse(self.espece.actif)
		self.assertTrue(Espece.objects.filter(pk=self.espece.id).exists())
