from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="events", default = 1)
    participants = models.ManyToManyField(User, related_name="events")
    confirm_participants = models.ManyToManyField(User, related_name="confirmed_events")

    def __str__(self):
        return self.name
    

# class Participant(models.Model):
#     name = models.CharField(max_length=150)
#     email = models.EmailField(max_length=250, unique=True)
#     events = models.ManyToManyField(Event, related_name="participants")