from django.db import models

NULLABLE = {"null": True, "blank": True}


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название курса")
    preview = models.ImageField(
        upload_to="materials/preview", **NULLABLE, verbose_name="Превью курса"
    )
    description = models.CharField(max_length=300, verbose_name="Описание курса")
    owner = models.ForeignKey("users.User", on_delete=models.SET_NULL, **NULLABLE, verbose_name="Владелец")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, **NULLABLE, related_name="lessons"
    )
    title = models.CharField(max_length=150, verbose_name="Название урока")
    description = models.CharField(max_length=300, verbose_name="Описание урока")
    preview = models.ImageField(
        upload_to="materials/preview", **NULLABLE, verbose_name="Превью урока"
    )
    video_url = models.URLField(**NULLABLE, verbose_name="Ссылка на видео")
    owner = models.ForeignKey("users.User", on_delete=models.SET_NULL, **NULLABLE, verbose_name="Владелец")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "course")
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"