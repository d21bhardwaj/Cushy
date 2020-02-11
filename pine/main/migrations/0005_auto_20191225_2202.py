# Generated by Django 2.2.2 on 2019-12-25 16:32

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20191024_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.ImageField(upload_to=main.models.user_directory_path, validators=[main.models.validate_image], verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='imagespg',
            name='image',
            field=models.ImageField(upload_to=main.models.user_directory_path_pg, validators=[main.models.validate_image], verbose_name='ImagePG'),
        ),
    ]