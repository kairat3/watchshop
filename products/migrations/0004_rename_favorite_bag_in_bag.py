# Generated by Django 3.2.4 on 2021-06-28 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_bag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bag',
            old_name='favorite',
            new_name='in_bag',
        ),
    ]
