from django.db import migrations


def sync_active_flags(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    for user in User.objects.all().iterator():
        user.is_active = user.actif
        user.save(update_fields=['is_active'])


def reverse_sync_active_flags(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    for user in User.objects.all().iterator():
        user.actif = user.is_active
        user.save(update_fields=['actif'])


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(sync_active_flags, reverse_sync_active_flags),
    ]
