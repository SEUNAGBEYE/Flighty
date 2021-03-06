# Generated by Django 2.1.5 on 2019-02-07 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='flight_class',
            field=models.CharField(choices=[('economy', 'Economy'), ('premium', 'Premium'), ('business', 'Business'), ('first_class', 'First Class')], default='economy', max_length=100),
        ),
        migrations.AddField(
            model_name='flight',
            name='travellers_capacity',
            field=models.IntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='flight',
            name='return_date',
            field=models.DateTimeField(blank=True),
        ),
    ]
