from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('debarquements', '0004_debarquement_validation'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='debarquement',
            name='archive',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='debarquement',
            name='archive_le',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='debarquement',
            name='archive_par',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='debarquements_archives',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]