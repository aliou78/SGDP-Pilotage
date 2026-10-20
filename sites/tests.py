from django.test import TestCase
from django.urls import reverse

from accounts.models import User

from .models import Site


class SiteActivationTests(TestCase):
	def setUp(self):
		self.admin = User.objects.create_user(
			username='admin',
			password='password123',
			role='admin',
		)
		self.site = Site.objects.create(
			nom='Site test',
			commune='Commune test',
			region='Region test',
		)

	def test_activation_requires_post(self):
		self.client.force_login(self.admin)
		url = reverse('site_toggle_active', kwargs={'pk': self.site.id})

		response = self.client.get(url)

		self.assertEqual(response.status_code, 405)

	def test_activation_post_toggles_site_without_deleting_it(self):
		self.client.force_login(self.admin)
		url = reverse('site_toggle_active', kwargs={'pk': self.site.id})

		response = self.client.post(url)

		self.assertRedirects(response, reverse('site_list'))
		self.site.refresh_from_db()
		self.assertFalse(self.site.actif)
		self.assertTrue(Site.objects.filter(pk=self.site.id).exists())
