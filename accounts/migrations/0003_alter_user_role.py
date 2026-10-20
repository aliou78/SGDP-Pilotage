from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0002_sync_active_flags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(
                choices=[
                    ('admin', 'Administrateur'),
                    ('chef', 'Chef de Service'),
                    ('agent', 'Agent de Collecte'),
                    ('consultation', 'Consultation'),
                ],
                default='agent',
                max_length=20,
            ),
        ),
    ]
