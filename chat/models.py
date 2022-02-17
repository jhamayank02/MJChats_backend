from django.db import models
from datetime import datetime

# Create your models here.
class Room(models.Model):
    room_code = models.TextField()
    room_creator = models.TextField()
    room_pass = models.TextField()
    room_id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.room_code + " created by " + self.room_creator

class Message(models.Model):
    sent_by = models.TextField()
    sent_on = models.TextField(default=datetime.now)
    msg = models.TextField()
    sent_to_room = models.TextField()

    def __str__(self):
        return self.sent_by + " to room " + self.sent_to_room
    
    