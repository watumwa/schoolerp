# Generated by Django 3.2.5 on 2024-07-01 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staffs', '0003_staff_clas'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staff',
            old_name='clas',
            new_name='class_taught',
        ),
    ]
