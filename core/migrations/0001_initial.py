# Generated by Django 4.2.5 on 2023-09-27 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True, null=True)),
                ('subtitle', models.CharField(blank=True, max_length=30, null=True)),
                ('language', models.CharField(blank=True, max_length=30, null=True)),
                ('pubDate', models.DateTimeField(blank=True, null=True)),
                ('duration', models.CharField(blank=True, max_length=50, null=True)),
                ('image', models.URLField(blank=True, null=True)),
                ('owner', models.BooleanField(null=True)),
                ('author', models.TextField()),
                ('source', models.URLField(blank=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.category')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='XmlLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xml_link', models.URLField(unique=True)),
                ('rss_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.type')),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('guid', models.CharField(max_length=200)),
                ('pubDate', models.DateTimeField(blank=True, null=True)),
                ('image', models.URLField(blank=True, null=True)),
                ('source', models.URLField(blank=True, null=True)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.channel')),
            ],
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('subtitle', models.CharField(blank=True, max_length=30, null=True)),
                ('guid', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('pubDate', models.DateTimeField(blank=True, null=True)),
                ('duration', models.CharField(blank=True, max_length=50, null=True)),
                ('audio_file', models.URLField()),
                ('image', models.URLField(blank=True, null=True)),
                ('explicit', models.BooleanField(blank=True, null=True)),
                ('channel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.channel')),
            ],
        ),
    ]
