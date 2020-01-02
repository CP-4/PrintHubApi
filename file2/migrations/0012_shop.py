# Generated by Django 2.2.5 on 2020-01-01 12:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('file2', '0011_auto_20191216_1240'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='err', max_length=200)),
                ('gmap_url', models.URLField(default='err', max_length=1000)),
                ('city', models.CharField(default='err', max_length=200)),
                ('state', models.CharField(default='err', max_length=200)),
                ('address', models.CharField(default='err', max_length=1000)),
                ('price_ss', models.FloatField(default=0)),
                ('price_ds', models.FloatField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
