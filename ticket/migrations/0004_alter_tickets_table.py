# Generated by Django 4.1.2 on 2022-11-02 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0003_rename_ticketdepartment_department_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='tickets',
            table='ticket',
        ),
    ]
