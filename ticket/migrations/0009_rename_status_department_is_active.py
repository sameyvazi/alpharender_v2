# Generated by Django 4.1.2 on 2022-11-02 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0008_alter_department_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='department',
            old_name='status',
            new_name='is_active',
        ),
    ]
