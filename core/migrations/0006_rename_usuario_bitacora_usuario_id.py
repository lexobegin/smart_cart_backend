# Generated by Django 5.2 on 2025-04-20 01:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_bitacora_usuario'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bitacora',
            old_name='usuario',
            new_name='usuario_id',
        ),
    ]
