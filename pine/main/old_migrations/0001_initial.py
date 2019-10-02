# Generated by Django 2.2.1 on 2019-06-05 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RentingUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('contact_number', models.CharField(max_length=10)),
                ('number_of_rooms', models.IntegerField()),
                ('locality', models.CharField(max_length=100)),
                ('parking', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3)),
                ('balcony', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3)),
                ('individual', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3)),
                ('attached_bathroom', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3)),
                ('kitchen', models.CharField(choices=[('furnished', 'Furnished'), ('basic', 'Basic')], max_length=15)),
                ('contact_time', models.CharField(max_length=50)),
                ('prefered_customer', models.CharField(max_length=20)),
                ('gender_pref', models.CharField(choices=[('female', 'Female'), ('male', 'Male'), ('none', 'None')], max_length=10)),
                ('Paying_guest', models.BooleanField()),
                ('people_per_room', models.IntegerField()),
                ('food', models.CharField(choices=[('included', 'Included'), ('not included', 'Not Included')], max_length=3)),
            ],
        ),
    ]