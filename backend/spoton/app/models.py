from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Feedback(models.Model):
    username = models.CharField(max_length=30)
    rating = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ])
    created_at = models.DateTimeField(auto_now_add=True)

class Help(models.Model):
    username = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False)

class Message(models.Model):
    body = models.CharField(max_length=100000)
    is_me = models.BooleanField()
    tag = models.CharField(max_length=100)
    username = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)



class Booking(models.Model):
    flight_id = models.CharField(max_length=1000)
    username = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
