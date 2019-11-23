from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import get_user_model
import os
from django.utils.translation import ugettext_lazy as _

import xml.dom.minidom
import zipfile
import re
import io
from PyPDF2 import PdfFileReader

# Create your models here.

# Link used to replace username with email
# https://www.fomfus.com/articles/how-to-use-email-as-username-for-django-authentication-removing-the-username

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class CustomUser(AbstractUser):
    student_name = models.CharField(max_length=100, default='student_name')
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['student_name']

    objects = UserManager()


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
    docname = models.CharField(max_length=100, default='docname')
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
        filename = filename.split('/')[-1]
        return filename+file_extension

    def get_document_pages(self):
        filename, file_extension = os.path.splitext(self.docfile.name)

        if file_extension == '.doc' or file_extension == '.docx':
            with zipfile.ZipFile(self.docfile) as document:
                uglyXml = xml.dom.minidom.parseString(document.read('docProps/app.xml')).toprettyxml(indent='  ')
                result = re.search('<Pages>(.*)</Pages>', uglyXml)
                pages = result.group(1)

            return pages

        elif file_extension == '.pdf':
            filebytes = self.docfile.read()
            # self.docfile.close()
            file = io.BytesIO(filebytes)
            pdf = PdfFileReader(file)
            pages = pdf.getNumPages()
            return pages


    def save(self, *args, **kwargs):

        self.doctype = self.get_document_type()
        self.docname = self.get_document_name()
        self.pages = self.get_document_pages()
        self.student_name = self.student.student_name
        super().save(*args, **kwargs)  # Call the "real" save() method.
