from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
import os


# Create your models here.

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class CustomUser(AbstractUser):
    pass


class Document(models.Model):

    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    printJobStatus = models.IntegerField(default=0)
    pages = models.IntegerField(default=0)
    doctype = models.CharField(max_length=5, default='err')

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
    )

    def get_document_type(self):
        filename, file_extension = os.path.splitext(self.docfile.name)
        print(self.docfile.name)
        print(filename, file_extension)
        return file_extension

    def save(self, *args, **kwargs):

        self.doctype = self.get_document_type()
        super().save(*args, **kwargs)  # Call the "real" save() method.
