# Generated by Django 3.2.4 on 2021-07-14 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20210707_2147'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-created_date', 'upvotes')},
        ),
        migrations.AddField(
            model_name='post',
            name='upvotes',
            field=models.IntegerField(default=0),
        ),
    ]
