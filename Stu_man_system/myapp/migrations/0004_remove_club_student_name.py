# Generated by Django 5.1.1 on 2024-10-11 01:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_book_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='club',
            name='student_name',
        ),
    ]
