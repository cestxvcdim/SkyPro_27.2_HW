from django.db import models


class Ad(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=20)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=500)
    address = models.CharField(max_length=100)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
