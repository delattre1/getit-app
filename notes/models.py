from django.db import models
# Create your models here.


class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    tag = models.CharField(max_length=50)

    def __str__(self):
        return self.title
