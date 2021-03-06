# Generated by Django 3.1.3 on 2020-11-12 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketModel', '0004_airplane_company_flight_information_ticket'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='airplane',
            name='id',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='id',
        ),
        migrations.AlterField(
            model_name='airplane',
            name='airplaneNumber',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='flight',
            name='flightNumber',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='airplaneNumber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticketModel.airplane'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='flightNumber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticketModel.flight'),
        ),
    ]
