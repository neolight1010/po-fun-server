# Generated by Django 3.2.5 on 2021-10-14 18:23

from django.db import migrations, models
import upload_validator


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0002_auto_20210709_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='demo',
            field=models.FileField(blank=True, upload_to='uploads/', validators=[upload_validator.FileTypeValidator(allowed_types=['audio/wav', 'audio/ogg', 'audio/mpeg'])]),
        ),
        migrations.AlterField(
            model_name='sample',
            name='file',
            field=models.FileField(upload_to='uploads/', validators=[upload_validator.FileTypeValidator(allowed_types=['audio/wav', 'audio/ogg', 'audio/mpeg'])]),
        ),
    ]