from django.db import models


class Urls(models.Model):
    shortenedUrl = models.CharField(verbose_name="shortenedUrl", max_length=256)
    urlToShorten = models.CharField(verbose_name="urlToShorten", max_length=256)
    views = models.IntegerField(verbose_name="views")
    rand_id = models.IntegerField(verbose_name="rand_id", db_index=True, unique=True)

    def __str__(self):
        return self.name
