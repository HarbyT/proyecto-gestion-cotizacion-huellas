from django import forms
from .models import Producto, Categoria

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre', 'descripcion', 'categoria', 'subcategoria',
            'tipo_papel', 'gramaje', 'tamaño', 'numero_paginas',
            'tipo_encuadernacion', 'acabados_especiales',
            'imagen_principal', 'imagenes_adicionales',
            'plantilla_ejemplo', 'precio_base', 'activo'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Tarjetas de presentación premium'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe las características principales del producto...'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'subcategoria': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Tarjetas ejecutivas, Tarjetas estándar'
            }),
            'tipo_papel': forms.Select(attrs={
                'class': 'form-select'
            }),
            'gramaje': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 300',
                'min': '1',
                'max': '1000'
            }),
            'tamaño': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 9x5 cm, A4, Carta'
            }),
            'numero_paginas': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 1, 4, 8, 16',
                'min': '1'
            }),
            'tipo_encuadernacion': forms.Select(attrs={
                'class': 'form-select'
            }),
            'acabados_especiales': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ej: Barniz UV selectivo, Laminado mate, Hot stamping dorado...'
            }),
            'imagen_principal': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'imagenes_adicionales': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'URLs de imágenes separadas por comas'
            }),
            'plantilla_ejemplo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.ai,.psd,.jpg,.png'
            }),
            'precio_base': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'nombre': 'Nombre del Producto',
            'descripcion': 'Descripción',
            'categoria': 'Categoría',
            'subcategoria': 'Subcategoría',
            'tipo_papel': 'Tipo de Papel',
            'gramaje': 'Gramaje (gramos)',
            'tamaño': 'Tamaño',
            'numero_paginas': 'Número de Páginas',
            'tipo_encuadernacion': 'Tipo de Encuadernación',
            'acabados_especiales': 'Acabados Especiales',
            'imagen_principal': 'Imagen Principal',
            'imagenes_adicionales': 'Imágenes Adicionales',
            'plantilla_ejemplo': 'Plantilla de Ejemplo',
            'precio_base': 'Precio Base',
            'activo': 'Producto Activo',
        }
        help_texts = {
            'gramaje': 'Peso del papel en gramos por metro cuadrado',
            'tamaño': 'Dimensiones del producto terminado',
            'numero_paginas': 'Total de páginas del producto final',
            'acabados_especiales': 'Describe procesos adicionales como barnices, laminados, etc.',
            'imagenes_adicionales': 'URLs de imágenes complementarias, separadas por comas',
            'plantilla_ejemplo': 'Archivo de ejemplo para el cliente (PDF, AI, PSD)',
            'precio_base': 'Precio de referencia para cotizaciones',
            'activo': 'Solo los productos activos aparecen en el catálogo público'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer algunos campos requeridos
        self.fields['nombre'].required = True
        self.fields['categoria'].required = True
        
        # Configurar queryset para categorías activas
        self.fields['categoria'].queryset = Categoria.objects.filter(activa=True)
        
        # Agregar clases CSS adicionales según el estado
        for field_name, field in self.fields.items():
            if field.required:
                if hasattr(field.widget, 'attrs'):
                    field.widget.attrs.update({'required': True})

    def clean_gramaje(self):
        gramaje = self.cleaned_data.get('gramaje')
        if gramaje and (gramaje < 1 or gramaje > 1000):
            raise forms.ValidationError('El gramaje debe estar entre 1 y 1000 gramos.')
        return gramaje

    def clean_numero_paginas(self):
        paginas = self.cleaned_data.get('numero_paginas')
        if paginas and paginas < 1:
            raise forms.ValidationError('El número de páginas debe ser mayor a 0.')
        return paginas

    def clean_precio_base(self):
        precio = self.cleaned_data.get('precio_base')
        if precio and precio < 0:
            raise forms.ValidationError('El precio no puede ser negativo.')
        return precio

    def clean_imagenes_adicionales(self):
        imagenes = self.cleaned_data.get('imagenes_adicionales', '')
        if imagenes:
            urls = [url.strip() for url in imagenes.split(',') if url.strip()]
            # Validar que sean URLs válidas
            for url in urls:
                if not (url.startswith('http://') or url.startswith('https://')):
                    raise forms.ValidationError(f'URL inválida: {url}. Debe empezar con http:// o https://')
        return imagenes


class ProductoFilterForm(forms.Form):
    search = forms.CharField(
        required=False,
        label='Buscar',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar productos...'
        })
    )
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(activa=True),
        required=False,
        label='Categoría',
        empty_label="Todas las categorías",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    tipo_papel = forms.ChoiceField(
        choices=[('', 'Todos los tipos')] + Producto.TIPOS_PAPEL,
        required=False,
        label='Tipo de Papel',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    activo = forms.ChoiceField(
        choices=[
            ('', 'Todos'),
            ('true', 'Activos'),
            ('false', 'Inactivos'),
        ],
        required=False,
        label='Estado',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    gramaje_min = forms.IntegerField(
        required=False,
        label='Gramaje mínimo',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 90',
            'min': '1'
        })
    )
    gramaje_max = forms.IntegerField(
        required=False,
        label='Gramaje máximo',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 300',
            'min': '1'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        gramaje_min = cleaned_data.get('gramaje_min')
        gramaje_max = cleaned_data.get('gramaje_max')

        if gramaje_min and gramaje_max and gramaje_min > gramaje_max:
            raise forms.ValidationError('El gramaje mínimo no puede ser mayor al máximo.')

        return cleaned_data


class CategoriaForm(forms.ModelForm):
    """Formulario para crear/editar categorías"""
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'activa']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Papelería Comercial'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe el tipo de productos de esta categoría...'
            }),
            'activa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'nombre': 'Nombre de la Categoría',
            'descripcion': 'Descripción',
            'activa': 'Categoría Activa',
        }
        help_texts = {
            'nombre': 'Nombre único para identificar la categoría',
            'descripcion': 'Información adicional sobre los productos de esta categoría',
            'activa': 'Solo las categorías activas aparecen en los filtros'
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            # Verificar que no exista otra categoría con el mismo nombre
            qs = Categoria.objects.filter(nombre__iexact=nombre)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('Ya existe una categoría con este nombre.')
        return nombre


class ProductoBulkActionForm(forms.Form):
    """Formulario para acciones masivas en productos"""
    ACTIONS = [
        ('activate', 'Activar productos'),
        ('deactivate', 'Desactivar productos'),
        ('delete', 'Eliminar productos'),
        ('change_category', 'Cambiar categoría'),
    ]
    
    action = forms.ChoiceField(
        choices=ACTIONS,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(activa=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    productos = forms.CharField(widget=forms.HiddenInput())

    def clean_productos(self):
        productos_ids = self.cleaned_data.get('productos', '')
        if not productos_ids:
            raise forms.ValidationError('Debes seleccionar al menos un producto.')
        
        try:
            ids = [int(id_str) for id_str in productos_ids.split(',') if id_str.strip()]
            if not ids:
                raise ValueError
        except ValueError:
            raise forms.ValidationError('IDs de productos inválidos.')
        
        return productos_ids

    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get('action')
        categoria = cleaned_data.get('categoria')
        
        if action == 'change_category' and not categoria:
            raise forms.ValidationError('Debes seleccionar una categoría para cambiar.')
        
        return cleaned_data