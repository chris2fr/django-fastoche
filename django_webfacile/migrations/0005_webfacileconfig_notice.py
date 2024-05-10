# Generated by Django 5.0.3 on 2024-04-02 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "django_webfacile",
            "0004_webfacileconfig_beta_tag_webfacileconfig_operator_logo_alt_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="webfacileconfig",
            name="notice",
            field=models.CharField(
                blank=True,
                default="",
                max_length=200,
                verbose_name="Bandeau d’information importante",
            ),
        ),
    ]