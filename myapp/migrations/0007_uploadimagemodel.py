# Generated by Django 2.2 on 2019-05-11 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_delete_uploadimagemodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadImageModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]