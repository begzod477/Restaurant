# Generated by Django 5.1.1 on 2024-11-06 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0007_review_profession'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Booking',
        ),
        migrations.DeleteModel(
            name='Testimonial',
        ),
    ]