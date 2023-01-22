from django.db import models
from django.utils.timezone import now


class Article(models.Model):
    # user=models.ForeignKey(user)
    title=models.CharField(max_length=255)
    content=models.TextField()
    # created=models.DateTimeField()