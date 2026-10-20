from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from especes.models import Espece
from sites.models import Site
from .models import Debarquement

User = get_user_model()


class DebarquementRolePermissionTests(TestCase):
	def setUp(self):
		self.agent = User.objects.create_user(
			username='agent1', password='password123', role='agent'
		)
		self.other_agent = User.objects.create_user(
			username='agent2', password='password123', role='agent'
		)
		self.chef = User.objects.create_user(
			username='chef', password='password123', role='chef'
		)
		self.admin = User.objects.create_user(
			username='admin', password='password123', role='admin'
		)
		self.site = Site.objects.create(
			nom='Port de test', commune='Commune', region='Région'
		)
		self.espece = Espece.objects.create(nom='Espèce de test')
		self.own_debarquement = self.create_debarquement(self.agent)
		self.other_debarquement = self.create_debarquement(self.other_agent)

	def create_debarquement(self, agent):
		return Debarquement.objects.create(
			date='2026-01-01',
			site=self.site,
			espece=self.espece,
			quantite='10.00',
			agent=agent,
		)

	def test_agent_can_consult_all_debarquements(self):
		self.client.force_login(self.agent)

		response = self.client.get(reverse('debarquement_list'))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['debarquements'].count(), 2)
		self.assertEqual(
			self.client.get(reverse('debarquement_archive_list')).status_code,
			403,
		)

		detail_response = self.client.get(
			reverse(
				'debarquement_detail',
				kwargs={'pk': self.other_debarquement.pk},
			)
		)
		self.assertEqual(detail_response.status_code, 200)

	def test_agent_can_update_only_own_debarquement(self):
		self.client.force_login(self.agent)

		own_response = self.client.get(
			reverse(
				'debarquement_update',
				kwargs={'pk': self.own_debarquement.pk},
			)
		)
		other_response = self.client.get(
			reverse(
				'debarquement_update',
				kwargs={'pk': self.other_debarquement.pk},
			)
		)
		own_post_response = self.client.post(
			reverse(
				'debarquement_update',
				kwargs={'pk': self.own_debarquement.pk},
			),
			{
				'date': '2026-01-02',
				'site': self.site.pk,
				'espece': self.espece.pk,
				'quantite': '20.00',
				'observation': 'Modifié par son agent',
			},
		)
		other_post_response = self.client.post(
			reverse(
				'debarquement_update',
				kwargs={'pk': self.other_debarquement.pk},
			),
			{
				'date': '2026-01-02',
				'site': self.site.pk,
				'espece': self.espece.pk,
				'quantite': '20.00',
				'observation': 'Modification interdite',
			},
		)

		self.assertEqual(own_response.status_code, 200)
		self.assertEqual(other_response.status_code, 404)
		self.assertEqual(own_post_response.status_code, 302)
		self.assertEqual(other_post_response.status_code, 404)
		self.own_debarquement.refresh_from_db()
		self.other_debarquement.refresh_from_db()
		self.assertEqual(self.own_debarquement.quantite, 20)
		self.assertEqual(self.other_debarquement.quantite, 10)

	def test_chef_and_admin_can_manage_any_agent_debarquement(self):
		for user in (self.chef, self.admin):
			with self.subTest(role=user.role):
				debarquement = self.create_debarquement(self.other_agent)
				self.client.force_login(user)

				update_response = self.client.get(
					reverse(
						'debarquement_update',
						kwargs={'pk': debarquement.pk},
					)
				)
				delete_response = self.client.get(
					reverse(
						'debarquement_delete',
						kwargs={'pk': debarquement.pk},
					)
				)
				validate_response = self.client.post(
					reverse(
						'debarquement_validate',
						kwargs={'pk': debarquement.pk},
					)
				)
				delete_response = self.client.post(
					reverse(
						'debarquement_delete',
						kwargs={'pk': debarquement.pk},
					)
				)

				self.assertEqual(update_response.status_code, 200)
				self.assertEqual(delete_response.status_code, 302)
				self.assertEqual(validate_response.status_code, 302)
				debarquement.refresh_from_db()
				self.assertTrue(debarquement.archive)
				self.assertEqual(debarquement.archive_par, user)
				self.assertIsNotNone(debarquement.archive_le)

				active_response = self.client.get(
					reverse('debarquement_list')
				)
				archive_response = self.client.get(
					reverse('debarquement_archive_list')
				)
				self.assertNotIn(
					debarquement,
					active_response.context['debarquements'],
				)
				self.assertIn(
					debarquement,
					archive_response.context['debarquements'],
				)

				restore_response = self.client.post(
					reverse(
						'debarquement_restore',
						kwargs={'pk': debarquement.pk},
					)
				)
				self.assertEqual(restore_response.status_code, 302)
				debarquement.refresh_from_db()
				self.assertFalse(debarquement.archive)
				self.assertIsNotNone(debarquement.archive_le)
