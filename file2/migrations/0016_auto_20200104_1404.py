# Generated by Django 2.2.5 on 2020-01-04 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file2', '0015_document_print_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='docname',
            field=models.CharField(default='docname', max_length=500),
        ),
    ]
