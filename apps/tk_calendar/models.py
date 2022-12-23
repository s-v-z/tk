from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
         return self.name

class Event(models.Model):
    author = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='authored_events')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_dt = models.DateTimeField()
    end_dt = models.DateTimeField()
    categories = models.ManyToManyField('Category', related_name='events')

    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
         return self.title