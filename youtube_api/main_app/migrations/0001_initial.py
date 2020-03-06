# Generated by Django 2.2.3 on 2019-07-23 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChannelDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=200)),
                ('subs', models.IntegerField()),
                ('videos_count', models.IntegerField()),
                ('profile_image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Setup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('link_video', models.TextField()),
                ('user_token', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='StatisticsDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('sentiment_result', models.ImageField(upload_to='')),
                ('most_positive_words', models.ImageField(upload_to='')),
                ('most_negative_words', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='VideoDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('likes', models.IntegerField()),
                ('dislikes', models.IntegerField()),
            ],
        ),
    ]