# Generated by Django 3.1.3 on 2020-11-12 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketModel', '0003_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Airplane',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('airplaneNumber', models.CharField(max_length=20)),
                ('craftTypeCode', models.IntegerField()),
                ('airlineName', models.CharField(max_length=20)),
                ('craftType', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=20)),
                ('site', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flightNumber', models.CharField(max_length=20)),
                ('departureCity', models.CharField(max_length=20)),
                ('arrivalCity', models.CharField(max_length=20)),
                ('departureTime', models.DateTimeField(null=True)),
                ('arrivalTime', models.DateTimeField(null=True)),
                ('departureAirportName', models.CharField(max_length=20)),
                ('arrivalAirportName', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flightNumber', models.CharField(max_length=20)),
                ('airplaneNumber', models.CharField(max_length=20)),
                ('company', models.CharField(max_length=20)),
                ('price', models.IntegerField()),
                ('ticketType', models.CharField(max_length=20)),
                ('returnRule', models.CharField(max_length=100)),
            ],
        ),
    ]
