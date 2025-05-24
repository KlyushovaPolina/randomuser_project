from django.db import models

class User(models.Model):
    gender = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    location = models.CharField(max_length=255)
    picture = models.URLField()