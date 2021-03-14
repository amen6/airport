from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Airport(models.Model):
    code = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.name} ({self.code})"

class Flight(models.Model):
    origin = models.ForeignKey('Airport', on_delete=models.CASCADE, related_name="From")
    destination = models.ForeignKey('Airport', on_delete=models.CASCADE,related_name="To")
    passengers = models.ManyToManyField('User', blank=True)
    def __str__(self):
        return f"{self.origin} to {self.destination}"

class Person(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    flights = models.ManyToManyField('Flight', blank=True)
    def __str__(self):
        return f"{self.user.username}"
