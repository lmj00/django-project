from django.db import models
from member.models import User
from shop.models import Post

# Create your models here.
class Room(models.Model):
    # post_id = models.ForeignKey(Post, on_delete=models.PROTECT)
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.IntegerField()
    user_id = models.IntegerField()
    last_content = models.TextField(blank=True)


class Message(models.Model):
    roomname = models.ForeignKey(Room, on_delete=models.PROTECT)
    content = models.TextField()       
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestmap = models.DateTimeField(auto_now=True)
