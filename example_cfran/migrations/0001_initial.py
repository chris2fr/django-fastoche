# Generated by Django 4.2.11 on 2024-05-07 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CfranAuthor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=250, verbose_name="First name"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=250, verbose_name="Last name"),
                ),
                (
                    "birth_date",
                    models.DateField(blank=True, null=True, verbose_name="Birth date"),
                ),
            ],
            options={
                "verbose_name": "cfran CfranAuthor",
            },
        ),
        migrations.CreateModel(
            name="CfranGenre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=15, verbose_name="Code")),
                (
                    "designation",
                    models.CharField(max_length=250, verbose_name="Designation"),
                ),
                (
                    "help_text",
                    models.CharField(
                        blank=True, max_length=250, verbose_name="Help text"
                    ),
                ),
            ],
            options={
                "verbose_name": "cfran CfranGenre",
            },
        ),
        migrations.CreateModel(
            name="CfranBook",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=250, verbose_name="Title")),
                (
                    "number_of_pages",
                    models.CharField(
                        blank=True, max_length=6, verbose_name="Number of pages"
                    ),
                ),
                (
                    "book_format",
                    models.CharField(
                        blank=True,
                        choices=[("PAPER", "Paper"), ("NUM", "Digital")],
                        max_length=10,
                        verbose_name="Format",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="example_cfran.cfranauthor",
                    ),
                ),
                ("genre", models.ManyToManyField(to="example_cfran.cfrangenre")),
            ],
            options={
                "verbose_name": "cfran CfranBook",
            },
        ),
    ]