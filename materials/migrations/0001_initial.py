# Generated by Django 4.2.2 on 2024-11-10 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
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
                    "title",
                    models.CharField(max_length=150, verbose_name="Название курса"),
                ),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="materials/preview",
                        verbose_name="Превью курса",
                    ),
                ),
                (
                    "description",
                    models.CharField(max_length=300, verbose_name="Описание курса"),
                ),
            ],
            options={
                "verbose_name": "Курс",
                "verbose_name_plural": "Курсы",
            },
        ),
        migrations.CreateModel(
            name="Lesson",
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
                    "title",
                    models.CharField(max_length=150, verbose_name="Название урока"),
                ),
                (
                    "description",
                    models.CharField(max_length=300, verbose_name="Описание урока"),
                ),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="materials/preview",
                        verbose_name="Превью урока",
                    ),
                ),
                (
                    "video_reference",
                    models.URLField(
                        blank=True, null=True, verbose_name="Ссылка на видео"
                    ),
                ),
            ],
            options={
                "verbose_name": "Урок",
                "verbose_name_plural": "Уроки",
            },
        ),
    ]
