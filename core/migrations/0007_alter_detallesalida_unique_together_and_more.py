# Generated by Django 5.2 on 2025-04-20 01:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_rename_usuario_bitacora_usuario_id'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='detallesalida',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='productoatributo',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='notasalida',
            name='productos',
        ),
    ]
