# Generated by Django 4.1.1 on 2022-10-24 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0005_keyfield"),
    ]

    operations = [
        migrations.RenameField(
            model_name="keyfield",
            old_name="key",
            new_name="skey",
        ),
    ]
