from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Document(models.Model):

	docfile = models.FileField(upload_to='documents/%Y/%m/%d')
	printJobStatus = models.IntegerField(default=0)


class CustomUser(AbstractUser):
	pass
