# Generated by Django 2.2.5 on 2019-11-14 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file2', '0002_document_doctype'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='student_name',
            field=models.CharField(default='student_name', max_length=100),
        ),
        migrations.AddField(
            model_name='document',
            name='docname',
            field=models.CharField(default='docname', max_length=100),
        ),
        migrations.AddField(
            model_name='document',
            name='print_copies',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='document',
            name='print_feature',
            field=models.CharField(choices=[('SINGLESIDE', 'Single Side'), ('DOUBLESIDE', 'Double Side'), ('BOOKSINGLESIDE', 'Book Single Side'), ('BOOKDOUBLESIDE', 'Book Double Side')], default='SINGLESIDE', max_length=20),
        ),
        migrations.AddField(
            model_name='document',
            name='student_name',
            field=models.CharField(default='student_name', max_length=100),
        ),
    ]
