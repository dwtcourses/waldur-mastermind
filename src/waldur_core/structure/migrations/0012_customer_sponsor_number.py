# Generated by Django 2.2.10 on 2020-06-02 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0011_allow_duplicate_agreement_numbers'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='sponsor_number',
            field=models.PositiveIntegerField(
                blank=True,
                help_text='External ID of the sponsor covering the costs',
                null=True,
            ),
        ),
    ]
