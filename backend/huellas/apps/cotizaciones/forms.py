from django import forms
from django.forms import inlineformset_factory
from .models import Cotizacion, DetalleCotizacion
from apps.clientes.models import Cliente
from apps.productos.models import Producto

class CotizacionForm(forms.ModelForm):
    """Formulario para crear/editar cotizaciones"""
    
    class Meta:
        model = Cotizacion
        fields = [
            'cliente', 
            'descripcion', 
            'observaciones',
            'condiciones_pago',
            'tiempo_entrega',
            'descuento_porcentaje',
            'iva_porcentaje',
            'fecha_vencimiento'
        ]
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción general de la cotización...'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales...'
            }),
            'condiciones_pago': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Ej: 50% anticipo, 50% contra entrega'
            }),
            'tiempo_entrega': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 5-7 días hábiles'
            }),
            'descuento_porcentaje': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'step': 0.01
            }),
            'iva_porcentaje': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'step': 0.01
            }),
            'fecha_vencimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configurar queryset de clientes activos
        self.fields['cliente'].queryset = Cliente.objects.filter(activo=True).order_by('nombre')
        
        # Hacer algunos campos opcionales
        self.fields['descripcion'].required = False
        self.fields['observaciones'].required = False
        self.fields['condiciones_pago'].required = False
        self.fields['tiempo_entrega'].required = False
        
        # Configurar labels
        self.fields['cliente'].label = "Cliente"
        self.fields['descripcion'].label = "Descripción"
        self.fields['observaciones'].label = "Observaciones"
        self.fields['condiciones_pago'].label = "Condiciones de pago"
        self.fields['tiempo_entrega'].label = "Tiempo de entrega"
        self.fields['descuento_porcentaje'].label = "Descuento general (%)"
        self.fields['iva_porcentaje'].label = "IVA (%)"
        self.fields['fecha_vencimiento'].label = "Fecha de vencimiento"

class DetalleCotizacionForm(forms.ModelForm):
    """Formulario para detalles de cotización"""
    
    class Meta:
        model = DetalleCotizacion
        fields = [
            'producto',
            'nombre_producto',
            'descripcion',
            'cantidad',
            'costo_unitario',
            'margen_utilidad',
            'precio_unitario',
            'descuento_porcentaje',
            'iva_porcentaje',
            'especificaciones_tecnicas',
            'observaciones'
        ]
        widgets = {
            'producto': forms.Select(attrs={
                'class': 'form-select producto-select'
            }),
            'nombre_producto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción del producto'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control cantidad-input',
                'min': 1,
                'value': 1
            }),
            'costo_unitario': forms.NumberInput(attrs={
                'class': 'form-control costo-input',
                'min': 0,
                'step': 0.01
            }),
            'margen_utilidad': forms.NumberInput(attrs={
                'class': 'form-control margen-input',
                'min': 0,
                'max': 1000,
                'step': 0.01,
                'value': 30
            }),
            'precio_unitario': forms.NumberInput(attrs={
                'class': 'form-control precio-input',
                'min': 0,
                'step': 0.01,
                'readonly': True
            }),
            'descuento_porcentaje': forms.NumberInput(attrs={
                'class': 'form-control descuento-input',
                'min': 0,
                'max': 100,
                'step': 0.01,
                'value': 0
            }),
            'iva_porcentaje': forms.NumberInput(attrs={
                'class': 'form-control iva-input',
                'min': 0,
                'max': 100,
                'step': 0.01,
                'value': 19
            }),
            'especificaciones_tecnicas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Especificaciones técnicas del producto'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones específicas'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configurar queryset de productos activos
        self.fields['producto'].queryset = Producto.objects.filter(activo=True).order_by('nombre')
        
        # Hacer algunos campos opcionales
        self.fields['descripcion'].required = False
        self.fields['especificaciones_tecnicas'].required = False
        self.fields['observaciones'].required = False
        
        # Configurar labels
        self.fields['producto'].label = "Producto"
        self.fields['nombre_producto'].label = "Nombre"
        self.fields['descripcion'].label = "Descripción"
        self.fields['cantidad'].label = "Cantidad"
        self.fields['costo_unitario'].label = "Costo unitario"
        self.fields['margen_utilidad'].label = "Margen (%)"
        self.fields['precio_unitario'].label = "Precio unitario"
        self.fields['descuento_porcentaje'].label = "Descuento (%)"
        self.fields['iva_porcentaje'].label = "IVA (%)"
        self.fields['especificaciones_tecnicas'].label = "Especificaciones"
        self.fields['observaciones'].label = "Observaciones"

# Formset para manejar múltiples detalles
DetalleCotizacionFormSet = inlineformset_factory(
    Cotizacion,
    DetalleCotizacion,
    form=DetalleCotizacionForm,
    extra=1,  # Número de formularios vacíos adicionales
    min_num=1,  # Mínimo un detalle
    validate_min=True,
    can_delete=True,  # Permitir eliminar detalles
    fields=[
        'producto',
        'nombre_producto', 
        'descripcion',
        'cantidad',
        'costo_unitario',
        'margen_utilidad',
        'precio_unitario',
        'descuento_porcentaje',
        'iva_porcentaje',
        'especificaciones_tecnicas',
        'observaciones'
    ]
)

class CotizacionBusquedaForm(forms.Form):
    """Formulario para buscar y filtrar cotizaciones"""
    
    ESTADOS_CHOICES = [('', 'Todos los estados')] + Cotizacion.ESTADOS
    
    codigo = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Código de cotización'
        })
    )
    
    cliente = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre del cliente'
        })
    )
    
    estado = forms.ChoiceField(
        choices=ESTADOS_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )