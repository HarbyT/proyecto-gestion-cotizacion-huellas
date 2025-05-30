# Generated by Django 5.1.3 on 2025-05-28 02:47

import apps.cotizaciones.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientes', '0001_initial'),
        ('productos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cotizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(default='COT-TEMP-0001', max_length=20, unique=True, verbose_name='Código')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True, verbose_name='Última actualización')),
                ('fecha_vencimiento', models.DateField(default=apps.cotizaciones.models.fecha_vencimiento_default, verbose_name='Fecha de vencimiento')),
                ('estado', models.CharField(choices=[('borrador', 'Borrador'), ('enviada', 'Enviada'), ('aceptada', 'Aceptada'), ('rechazada', 'Rechazada'), ('vencida', 'Vencida')], default='borrador', max_length=20, verbose_name='Estado')),
                ('descripcion', models.TextField(blank=True, verbose_name='Descripción')),
                ('observaciones', models.TextField(blank=True, verbose_name='Observaciones')),
                ('condiciones_pago', models.TextField(blank=True, verbose_name='Condiciones de pago')),
                ('tiempo_entrega', models.CharField(blank=True, max_length=100, verbose_name='Tiempo de entrega')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Subtotal')),
                ('descuento_porcentaje', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Descuento (%)')),
                ('descuento_valor', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Descuento ($)')),
                ('iva_porcentaje', models.DecimalField(decimal_places=2, default=19, max_digits=5, verbose_name='IVA (%)')),
                ('iva_valor', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='IVA ($)')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Total')),
                ('activo', models.BooleanField(default=True, verbose_name='Activo')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.cliente', verbose_name='Cliente')),
                ('usuario_creador', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
            ],
            options={
                'verbose_name': 'Cotización',
                'verbose_name_plural': 'Cotizaciones',
                'db_table': 'cotizacion',
                'ordering': ['-fecha_creacion'],
            },
        ),
        migrations.CreateModel(
            name='DetalleCotizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_producto', models.CharField(max_length=200, verbose_name='Nombre del producto')),
                ('descripcion', models.TextField(blank=True, verbose_name='Descripción')),
                ('cantidad', models.IntegerField(default=1, verbose_name='Cantidad')),
                ('costo_unitario', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Costo unitario')),
                ('margen_utilidad', models.DecimalField(decimal_places=2, default=30, max_digits=5, verbose_name='Margen de utilidad (%)')),
                ('precio_unitario', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Precio unitario')),
                ('descuento_porcentaje', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Descuento (%)')),
                ('descuento_valor', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Descuento ($)')),
                ('iva_porcentaje', models.DecimalField(decimal_places=2, default=19, max_digits=5, verbose_name='IVA (%)')),
                ('iva_valor', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='IVA ($)')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Subtotal')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Total')),
                ('especificaciones_tecnicas', models.TextField(blank=True, verbose_name='Especificaciones técnicas')),
                ('observaciones', models.TextField(blank=True, verbose_name='Observaciones')),
                ('cotizacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='cotizaciones.cotizacion', verbose_name='Cotización')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.producto', verbose_name='Producto')),
            ],
            options={
                'verbose_name': 'Detalle de cotización',
                'verbose_name_plural': 'Detalles de cotización',
                'db_table': 'detalle_cotizacion',
                'ordering': ['id'],
            },
        ),
    ]
