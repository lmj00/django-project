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

    CATEGROY_CHOICES = [
        ('디지털/가전', '디지털/가전'),
        ('가구/인테리어', '가구/인테리어'),
        ('생활/가공식품', '생활/가공식품'),
        ('뷰티/미용', '뷰티/미용'),
        ('패션/잡화', '패션/잡화'),
        ('게임/스포츠', '게임/스포츠'),
        ('반려동물용품', '반려동물용품'),
        ('기타', '기타'),
    ]

    category = models.CharField(max_length=20, choices=CATEGROY_CHOICES)
    

    def __str__(self):
        return self.title
