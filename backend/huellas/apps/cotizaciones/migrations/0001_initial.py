# Generated by Django 5.1.3 on 2024-12-02 00:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientes', '0001_initial'),
        ('productos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cotizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('aprobada', 'Aprobada'), ('completada', 'Completada')], max_length=50)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('iva', models.DecimalField(decimal_places=2, default=19.0, max_digits=5)),
                ('margen_ganancia', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleCotizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sub_total', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('cotizacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='cotizaciones.cotizacion')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.producto')),
            ],
        ),
    ]
