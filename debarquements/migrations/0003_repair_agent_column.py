from django.db import migrations


def add_agent_column(apps, schema_editor):
    connection = schema_editor.connection
    table_name = 'debarquements_debarquement'
    column_names = {
        column.name
        for column in connection.introspection.get_table_description(
            connection.cursor(),
            table_name,
        )
    }

    if 'agent_id' not in column_names:
        debarquement_model = apps.get_model('debarquements', 'Debarquement')
        schema_editor.add_field(
            debarquement_model,
            debarquement_model._meta.get_field('agent'),
        )


def remove_agent_column(apps, schema_editor):
    debarquement_model = apps.get_model('debarquements', 'Debarquement')
    connection = schema_editor.connection
    table_name = debarquement_model._meta.db_table
    column_names = {
        column.name
        for column in connection.introspection.get_table_description(
            connection.cursor(),
            table_name,
        )
    }

    if 'agent_id' in column_names:
        schema_editor.remove_field(
            debarquement_model,
            debarquement_model._meta.get_field('agent'),
        )


class Migration(migrations.Migration):

    dependencies = [
        ('debarquements', '0002_debarquement_agent'),
    ]

    operations = [
        migrations.RunPython(add_agent_column, remove_agent_column),
    ]
