# Generated by Django 4.2.20 on 2025-03-29 01:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clerk_user_id', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Voiture',
            fields=[
                ('id_voiture', models.AutoField(primary_key=True, serialize=False)),
                ('marque', models.CharField(max_length=255)),
                ('matricule', models.CharField(max_length=255, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='voitures/')),
            ],
        ),
        migrations.CreateModel(
            name='Trajet',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('phonenumber', models.CharField(max_length=8)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('departure', models.CharField(max_length=255)),
                ('arrival', models.CharField(max_length=255)),
                ('departure_date', models.DateTimeField()),
                ('arrival_date', models.DateTimeField()),
                ('nb_places', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('voiture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.voiture')),
            ],
        ),
    ]
