from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from debarquements.models import Debarquement
from especes.models import Espece
from sites.models import Site


class DashboardSpeciesFilterTests(TestCase):

	def test_species_selector_filters_dashboard_data(self):
		user = User.objects.create_user(
			username='dashboard_user',
			password='password123',
			role='agent',
		)
		site = Site.objects.create(
			nom='Dashboard site',
			commune='Dashboard commune',
			region='Dashboard region',
		)
		selected_species = Espece.objects.create(nom='Espèce sélectionnée')
		other_species = Espece.objects.create(nom='Autre espèce')
		Debarquement.objects.create(
			date='2026-01-01',
			site=site,
			espece=selected_species,
			quantite=20,
		)
		Debarquement.objects.create(
			date='2026-01-02',
			site=site,
			espece=other_species,
			quantite=80,
		)
		self.client.force_login(user)

		response = self.client.get(
			reverse('dashboard'),
			{'espece': selected_species.pk},
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['nombre_debarquements'], 1)
		self.assertEqual(response.context['quantite_totale'], 20)
		self.assertEqual(
			response.context['espece_selectionnee'],
			str(selected_species.pk),
		)
		self.assertContains(response, 'name="espece"')
		self.assertContains(response, 'Espèce sélectionnée')
