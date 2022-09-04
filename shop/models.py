from django.db import models
from django.core.validators import MinValueValidator
from member.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)

    content = models.TextField()

    address = models.CharField(max_length=30)

    price = models.IntegerField(
        validators=[MinValueValidator(1)]
    ) 

    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)

    image1 = models.ImageField(upload_to="post_pics")
    image2 = models.ImageField(upload_to="post_pics", blank=True)
    image3 = models.ImageField(upload_to="post_pics", blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    dt_created = models.DateTimeField(auto_now=True)
    
    is_sold = models.BooleanField(default=False)

    """ 
    카테고리 추가 예정
    """

    def __str__(self):
        return self.title
