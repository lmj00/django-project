from django.db import models
from member.models import User
from shop.models import Post

# Create your models here.
class Room(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer')
    last_content = models.TextField(blank=True)


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    content = models.TextField()       
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestmap = models.DateTimeField(auto_now=True)