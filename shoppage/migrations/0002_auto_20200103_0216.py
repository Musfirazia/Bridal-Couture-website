# Generated by Django 2.2.4 on 2020-01-02 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shoppage', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='phonenumber',
            new_name='number',
        ),
    ]
