# Generated by Django 2.2.1 on 2019-12-17 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(default='', max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default='', max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop', models.CharField(default='', max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(default='', max_length=40)),
                ('quantity', models.CharField(default='', max_length=10)),
                ('price', models.IntegerField(default='')),
                ('description', models.TextField(blank=True, max_length=100, null=True)),
                ('off', models.BooleanField(default=False)),
                ('savings', models.IntegerField(blank=True, null=True)),
                ('code', models.IntegerField(blank=True, null=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='grocery.Brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='grocery.Category')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grocery.Shop')),
            ],
        ),
    ]