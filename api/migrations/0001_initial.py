# Generated by Django 3.1.1 on 2022-04-10 07:21

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
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('first_name', models.CharField(max_length=30, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=30, verbose_name='Last Name')),
                ('country', models.CharField(max_length=30, verbose_name='Country Name')),
                ('player_type', models.CharField(max_length=30, verbose_name='Player Type')),
                ('initial_value', models.DecimalField(decimal_places=3, default=1.0, max_digits=6)),
                ('age', models.BigIntegerField(default=0)),
                ('market_value', models.BigIntegerField(default=1)),
                ('is_transferred', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='TransferList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('asking_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('status', models.CharField(choices=[('New', 'New'), ('Transferred', 'Transferred')], default='New', max_length=12)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfers', to='api.player')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transferring_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('team_name', models.CharField(max_length=30, verbose_name='Team Name')),
                ('team_country', models.CharField(max_length=30, verbose_name='Team Country')),
                ('team_value', models.DecimalField(decimal_places=3, default=20.0, max_digits=6)),
                ('additional_resource', models.DecimalField(decimal_places=3, default=5.0, max_digits=6)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='api.team'),
        ),
        migrations.AddIndex(
            model_name='transferlist',
            index=models.Index(fields=['player'], name='player_idx'),
        ),
        migrations.AddIndex(
            model_name='team',
            index=models.Index(fields=['team_name'], name='team_name_idx'),
        ),
        migrations.AddIndex(
            model_name='player',
            index=models.Index(fields=['country'], name='country__idx'),
        ),
    ]
