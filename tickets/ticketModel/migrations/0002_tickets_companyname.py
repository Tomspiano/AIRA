# Generated by Django 3.1.1 on 2020-11-26 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketModel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickets',
            name='companyName',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
