# Generated by Django 2.1.8 on 2019-05-16 04:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peopleNm', models.CharField(default='', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peopleNm', models.CharField(default='', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genreNm', models.CharField(default='', max_length=150)),
                ('selected', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movieCd', models.IntegerField(default=0)),
                ('movieNm', models.CharField(default='', max_length=150)),
                ('openDt', models.CharField(default='', max_length=150)),
                ('audiAcc', models.IntegerField(default=0)),
                ('movieNmEn', models.CharField(default='', max_length=150)),
                ('showTm', models.IntegerField(default=0)),
                ('posterUrl', models.CharField(default='', max_length=200)),
                ('description', models.TextField(default='')),
                ('score', models.FloatField(default=0)),
                ('trailer', models.CharField(default='', max_length=150)),
                ('watchGradeNm', models.CharField(default='', max_length=150)),
                ('selected', models.BooleanField(default=False)),
                ('actor', models.ManyToManyField(related_name='movies', to='movies.Actor')),
                ('director', models.ManyToManyField(related_name='movies', to='movies.Director')),
                ('genre', models.ManyToManyField(related_name='movies', to='movies.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='Nation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nationNm', models.CharField(default='', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(default='')),
                ('score', models.IntegerField(default=0)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='movies.Movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StillCut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stillCut', models.CharField(default='', max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='nation',
            field=models.ManyToManyField(related_name='movies', to='movies.Nation'),
        ),
        migrations.AddField(
            model_name='movie',
            name='stillCut',
            field=models.ManyToManyField(related_name='movies', to='movies.StillCut'),
        ),
    ]
