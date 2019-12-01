# Generated by Django 2.2.2 on 2019-10-26 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grocery', '0002_auto_20191026_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='code',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='savings',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
