# finalregapp/models.py

from django.db import models

class PDF(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='pdfs/')

    def __str__(self):
        return self.title
