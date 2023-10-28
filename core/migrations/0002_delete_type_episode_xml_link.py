# Generated by Django 4.2.5 on 2023-10-27 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Type',
        ),
        migrations.AddField(
            model_name='episode',
            name='xml_link',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='core.xmllink'),
            preserve_default=False,
        ),
    ]