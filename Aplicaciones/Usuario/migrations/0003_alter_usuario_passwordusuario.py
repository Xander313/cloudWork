# Generated by Django 5.2.1 on 2025-07-14 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuario', '0002_usuario_direccionusuario_usuario_telefonousuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='passwordUsuario',
            field=models.CharField(default='', max_length=100),
        ),
    ]
