# Generated by Django 3.2.4 on 2021-07-07 16:17

import blog.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20210704_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='note',
            field=models.FileField(upload_to='media', validators=[blog.validators.validate_file_extension]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='dp',
            field=models.ImageField(default='default.png', upload_to='images', validators=[blog.validators.validate_image_extension]),
        ),
    ]
