from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
import os


# Create your models here.

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class CustomUser(AbstractUser):
    student_name = models.CharField(max_length=100, default='student_name')
    pass


class Document(models.Model):

    SINGLESIDE = "SINGLESIDE"
    DOUBLESIDE = "DOUBLESIDE"
    BOOKSINGLESIDE = "BOOKSINGLESIDE"
    BOOKDOUBLESIDE = "BOOKDOUBLESIDE"

    PRINT_FEATURE_CHOICES = (
        (SINGLESIDE, "Single Side"),
        (DOUBLESIDE, "Double Side"),
        (BOOKSINGLESIDE, "Book Single Side"),
        (BOOKDOUBLESIDE, "Book Double Side"),
    )

    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    printJobStatus = models.IntegerField(default=0)
    pages = models.IntegerField(default=0)
    doctype = models.CharField(max_length=5, default='err')
    docname = models.CharField(max_length=20, default='docname')
    student_name = models.CharField(max_length=100, default='student_name')

    print_copies = models.IntegerField(default=1)
    print_feature = models.CharField(max_length=20, choices=PRINT_FEATURE_CHOICES, default=SINGLESIDE)

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
    )

    def get_document_type(self):
        filename, file_extension = os.path.splitext(self.docfile.name)
        return file_extension

    def get_document_name(self):
        filename, file_extension = os.path.splitext(self.docfile.name)
        return filename

    def save(self, *args, **kwargs):

        self.doctype = self.get_document_type()
        self.filename = self.get_document_name()
        self.student_name = self.student.student_name;
        super().save(*args, **kwargs)  # Call the "real" save() method.
