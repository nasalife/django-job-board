# Generated by Django 4.2.7 on 2023-11-14 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0008_job_slug_alter_job_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('website', models.URLField(max_length=100)),
                ('cv', models.FileField(upload_to='apply')),
                ('cover_letter', models.TextField(max_length=500)),
            ],
        ),
    ]
