from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class CustomUser(AbstractUser):
    n_code = models.IntegerField()
    phone = models.CharField(max_length=50)
