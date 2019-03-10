# Generated by Django 2.1.1 on 2018-10-18 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotator', '0011_remove_user_systemname'),
    ]

    operations = [
        migrations.CreateModel(
            name='approver_annotated_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resumeId', models.CharField(max_length=255)),
                ('userName', models.CharField(max_length=255)),
                ('approverName', models.CharField(max_length=255)),
                ('tagId', models.CharField(max_length=255)),
                ('annotaedData', models.CharField(max_length=5000)),
                ('action', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
