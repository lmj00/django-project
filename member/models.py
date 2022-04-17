from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_no_special_characters

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(
        max_length=15, 
        unique=True, 
        null=True,
        validators=[validate_no_special_characters],
        error_messages={'unique': '이미 사용중인 닉네임입니다.'},
    )

    address = models.CharField(
        max_length=15,
        null=True,
    )

    lat = models.FloatField(
        null=True
    )

    lon = models.FloatField(
        null=True
    )

    def __str__(self):
        return self.email


class AddressCSV(models.Model):
    code = models.CharField(
        max_length=15
    )

    name = models.CharField(
        max_length=25
    )

    status = models.CharField(
        max_length=5
    )


    class Meta:
        db_table = 'address_csv'