from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    location = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="events", default = 1)
    # participants

    def __str__(self):
        return self.name
    

class Participant(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=250, unique=True)
    events = models.ManyToManyField(Event, related_name="participants")