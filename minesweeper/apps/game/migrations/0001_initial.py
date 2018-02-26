# Generated by Django 2.0.2 on 2018-02-26 04:48

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
            name='Cell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mine', models.BooleanField(default=False)),
                ('visible', models.BooleanField(default=False)),
                ('sign', models.IntegerField(choices=[(0, ''), (1, '?'), (2, 'F')], default=0)),
                ('row', models.IntegerField(db_index=True)),
                ('column', models.IntegerField(db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=128)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('last_action', models.DateTimeField(auto_now=True)),
                ('elapsed_time', models.IntegerField(default=0)),
                ('status', models.IntegerField(choices=[(0, 'Paused'), (1, 'Playing'), (2, 'Lost'), (3, 'Won')], default=1)),
                ('rows', models.IntegerField(default=9)),
                ('columns', models.IntegerField(default=9)),
                ('mines', models.IntegerField(default=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='cell',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cells', to='game.Game'),
        ),
    ]