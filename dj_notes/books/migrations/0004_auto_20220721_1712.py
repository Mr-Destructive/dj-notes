# Generated by Django 3.2.13 on 2022-07-21 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20220607_1401'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=256)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='notebook',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, related_name='booktags', to='books.Tag'),
        ),
    ]
