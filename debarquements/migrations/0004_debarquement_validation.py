from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('debarquements', '0003_repair_agent_column'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='debarquement',
            name='statut',
            field=models.CharField(
                choices=[('en_attente', 'En attente'), ('valide', 'Validé')],
                default='en_attente',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='debarquement',
            name='valide_le',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='debarquement',
            name='valide_par',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='debarquements_valides',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
