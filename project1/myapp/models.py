from django.db import models


# Create your models here.
class CDetails(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField()
    dropdown = models.CharField(max_length=30)
    phone = models.CharField(max_length=10)
    texts = models.TextField()

    def __str__(self) -> str:
        return self.firstname
