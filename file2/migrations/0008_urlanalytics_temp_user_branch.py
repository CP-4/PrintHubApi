# Generated by Django 2.2.5 on 2019-12-04 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file2', '0007_gueststudent'),
    ]

    operations = [
        migrations.AddField(
            model_name='urlanalytics',
            name='temp_user_branch',
            field=models.CharField(default='err', max_length=50),
        ),
    ]
