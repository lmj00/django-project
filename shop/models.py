from email.mime import image
from django.db import models
from django.forms import CharField
from django.core.validators import MinValueValidator
from member.models import User


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)

    content = models.TextField()
    
    price = models.IntegerField(
        validators=[MinValueValidator(1)]
    ) 

    image1 = models.ImageField()
    image2 = models.ImageField(blank=True)
    image3 = models.ImageField(blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    dt_created = models.DateTimeField(auto_now=True)


    """ 
    카테고리 추가 예정
    """

    def __str__(self):
        return self.title
