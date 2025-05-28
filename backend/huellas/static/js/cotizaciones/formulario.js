// Variables globales
let detalleIndex = 0;
let productos = [];

// URLs para AJAX (se obtienen del template)
const URLS = window.COTIZACION_URLS || {
    buscarProductos: '/productos/ajax/buscar/',
    obtenerProducto: '/productos/ajax/',
    calcularPrecios: '/cotizaciones/ajax/calcular-precios/',
    listaProductos: '/productos/ajax/lista/'
};

// Inicialización del documento
document.addEventListener('DOMContentLoaded', function() {
    initFormulario();
    initBusquedaProductos();
    initCalculosAutomaticos();
    cargarProductos();
});

// Inicialización principal del formulario
function initFormulario() {
    // Contar detalles existentes
    const detallesExistentes = document.querySelectorAll('.detalle-form');
    detalleIndex = detallesExistentes.length;
    
    // Configurar eventos de cálculo
    document.addEventListener('input', function(e) {
        if (e.target.matches('[name*="costo_unitario"], [name*="margen_utilidad"], [name*="descuento_porcentaje"], [name*="iva_porcentaje"]')) {
            calcularTotales();
        }
    });
    
    // Configurar eventos de cambio
    document.addEventListener('change', function(e) {
        if (e.target.matches('[name*="incluir_iva"]')) {
            calcularTotales();
        }
    });
}

// Inicializar búsqueda de productos
function initBusquedaProductos() {
    document.addEventListener('input', function(e) {
        if (e.target.classList.contains('buscar-producto')) {
            buscarProductos(e.target);
        }
    });
    
    // Cerrar resultados al hacer clic fuera
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.buscar-producto') && !e.target.closest('.resultados-busqueda')) {
            ocultarResultadosBusqueda();
        }
    });
}

// Inicializar cálculos automáticos
function initCalculosAutomaticos() {
    // Calcular precios automáticamente al cambiar costo o margen
    document.addEventListener('input', function(e) {
        if (e.target.matches('[name*="costo_unitario"]') || e.target.matches('#id_margen_utilidad')) {
            const detalleForm = e.target.closest('.detalle-form');
            if (detalleForm) {
                calcularPrecioUnitario(detalleForm);
                mostrarTablaPrecios(detalleForm);
            }
        }
    });
}

// Cargar productos desde el servidor
async function cargarProductos() {
    try {
        const response = await fetch(URLS.listaProductos);
        if (response.ok) {
            productos = await response.json();
        }
    } catch (error) {
        console.error('Error cargando productos:', error);
    }
}

// Buscar productos usando la API de productos
async function buscarProductos(input) {
    const query = input.value.toLowerCase();
    const contenedorResultados = input.parentElement.nextElementSibling;
    
    if (query.length < 2) {
        contenedorResultados.style.display = 'none';
        return;
    }
    
    try {
        const response = await fetch(`${URLS.buscarProductos}?q=${encodeURIComponent(query)}`);
        if (response.ok) {
            const resultados = await response.json();
            mostrarResultadosBusqueda(contenedorResultados, resultados.slice(0, 5), input);
        }
    } catch (error) {
        console.error('Error buscando productos:', error);
        // Fallback a búsqueda local
        const resultados = productos.filter(producto => 
            producto.nombre.toLowerCase().includes(query) ||
            (producto.descripcion && producto.descripcion.toLowerCase().includes(query))
        ).slice(0, 5);
        
        mostrarResultadosBusqueda(contenedorResultados, resultados, input);
    }
}

// Mostrar resultados de búsqueda
function mostrarResultadosBusqueda(contenedor, resultados, input) {
    contenedor.innerHTML = '';
    
    if (resultados.length === 0) {
        contenedor.innerHTML = '<div class="p-2 text-muted">No se encontraron productos</div>';
    } else {
        resultados.forEach(producto => {
            const item = document.createElement('div');
            item.className = 'p-2 border-bottom cursor-pointer hover-bg-light';
            item.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <strong>${producto.nombre}</strong>
                        <br>
                        <small class="text-muted">${producto.categoria__nombre || ''}</small>
                    </div>
                    <small class="text-success">$${producto.precio_base || '0'}</small>
                </div>
            `;
            
            item.addEventListener('click', function() {
                seleccionarProducto(producto, input);
            });
            
            contenedor.appendChild(item);
        });
    }
    
    contenedor.style.display = 'block';
}

// Seleccionar producto
function seleccionarProducto(producto, inputBusqueda) {
    const detalleForm = inputBusqueda.closest('.detalle-form');
    const selectProducto = detalleForm.querySelector('select[name*="producto"]');
    
    // Actualizar el select
    const option = new Option(producto.nombre, producto.id, true, true);
    selectProducto.appendChild(option);
    selectProducto.value = producto.id;
    
    // Llenar campos automáticamente
    llenarCamposProducto(detalleForm, producto);
    
    // Ocultar resultados
    ocultarResultadosBusqueda();
    
    // Limpiar búsqueda
    inputBusqueda.value = '';
}

// Llenar campos del producto
function llenarCamposProducto(detalleForm, producto) {
    // Campos básicos
    const campos = {
        'tipo_papel': producto.tipo_papel,
        'gramaje': producto.gramaje,
        'tamaño_personalizado': producto.tamaño,
        'acabados_personalizados': producto.acabados_especiales,
        'costo_unitario': producto.precio_base ? (producto.precio_base * 0.7) : 0, // Estimación de costo
        'precio_unitario': producto.precio_base || 0
    };
    
    Object.entries(campos).forEach(([campo, valor]) => {
        const input = detalleForm.querySelector(`[name*="${campo}"]`);
        if (input && valor) {
            input.value = valor;
        }
    });
    
    // Recalcular después de llenar
    calcularPrecioUnitario(detalleForm);
    mostrarTablaPrecios(detalleForm);
}

// Ocultar resultados de búsqueda
function ocultarResultadosBusqueda() {
    document.querySelectorAll('.resultados-busqueda').forEach(contenedor => {
        contenedor.style.display = 'none';
    });
}

// Agregar nuevo detalle
function agregarDetalle() {
    const contenedor = document.getElementById('detalles-container');
    const managementForm = document.querySelector('#id_detalles-TOTAL_FORMS');
    const totalForms = parseInt(managementForm.value);
    
    // Clonar el último formulario
    const ultimoDetalle = document.querySelector('.detalle-form:last-of-type');
    const nuevoDetalle = ultimoDetalle.cloneNode(true);
    
    // Actualizar índices
    nuevoDetalle.setAttribute('data-index', totalForms);
    
    // Limpiar valores
    const inputs = nuevoDetalle.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        if (input.type !== 'hidden') {
            input.value = '';
        }
        // Actualizar nombres con nuevo índice
        if (input.name) {
            input.name = input.name.replace(/detalles-\d+/, `detalles-${totalForms}`);
            input.id = input.id.replace(/detalles-\d+/, `detalles-${totalForms}`);
        }
    });
    
    // Actualizar header
    const header = nuevoDetalle.querySelector('h6');
    header.textContent = `Producto ${totalForms + 1}`;
    
    // Agregar botón de eliminar
    const headerContainer = nuevoDetalle.querySelector('.d-flex.justify-content-between');
    if (!headerContainer.querySelector('.btn-outline-danger')) {
        const eliminarBtn = document.createElement('button');
        eliminarBtn.type = 'button';
        eliminarBtn.className = 'btn btn-outline-danger btn-sm';
        eliminarBtn.innerHTML = '<i class="bi bi-trash"></i>';
        eliminarBtn.onclick = function() { eliminarDetalle(this); };
        headerContainer.appendChild(eliminarBtn);
    }
    
    // Ocultar tabla de precios
    const tablaPrecios = nuevoDetalle.querySelector('.tabla-precios-container');
    if (tablaPrecios) {
        tablaPrecios.style.display = 'none';
    }
    
    // Agregar al contenedor
    contenedor.appendChild(nuevoDetalle);
    
    // Actualizar management form
    managementForm.value = totalForms + 1;
    
    // Reinicializar eventos
    initBusquedaProductos();
}

// Eliminar detalle
function eliminarDetalle(boton) {
    const detalleForm = boton.closest('.detalle-form');
    const managementForm = document.querySelector('#id_detalles-TOTAL_FORMS');
    
    // Marcar para eliminación si tiene ID
    const deleteCheckbox = detalleForm.querySelector('input[name*="DELETE"]');
    if (deleteCheckbox) {
        deleteCheckbox.checked = true;
        detalleForm.style.display = 'none';
    } else {
        // Remover completamente si es nuevo
        detalleForm.remove();
        
        // Actualizar management form
        const totalForms = parseInt(managementForm.value) - 1;
        managementForm.value = totalForms;
    }
    
    // Recalcular totales
    calcularTotales();
}

// Calcular precio unitario basado en costo y margen
function calcularPrecioUnitario(detalleForm) {
    const costoInput = detalleForm.querySelector('[name*="costo_unitario"]');
    const precioInput = detalleForm.querySelector('[name*="precio_unitario"]');
    const margenInput = document.querySelector('#id_margen_utilidad');
    
    if (costoInput && precioInput && margenInput) {
        const costo = parseFloat(costoInput.value) || 0;
        const margen = parseFloat(margenInput.value) || 30;
        
        if (costo > 0) {
            const precio = costo * (1 + margen / 100);
            precioInput.value = precio.toFixed(4);
        }
    }
}

// Mostrar tabla de precios
function mostrarTablaPrecios(detalleForm) {
    const costoInput = detalleForm.querySelector('[name*="costo_unitario"]');
    const margenInput = document.querySelector('#id_margen_utilidad');
    const tablaContainer = detalleForm.querySelector('.tabla-precios-container');
    const tablaBody = detalleForm.querySelector('.tabla-precios-body');
    
    if (!costoInput || !margenInput || !tablaContainer || !tablaBody) return;
    
    const costo = parseFloat(costoInput.value) || 0;
    const margen = parseFloat(margenInput.value) || 30;
    
    if (costo <= 0) {
        tablaContainer.style.display = 'none';
        return;
    }
    
    // Calcular precios para diferentes cantidades
    const cantidades = [50, 100, 200, 300, 500, 1000, 2000, 5000];
    const precioBase = costo * (1 + margen / 100);
    
    tablaBody.innerHTML = '';
    
    cantidades.forEach(cantidad => {
        // Aplicar descuentos por volumen
        let descuento = 0;
        if (cantidad >= 1000) descuento = 0.15;
        else if (cantidad >= 500) descuento = 0.10;
        else if (cantidad >= 200) descuento = 0.05;
        
        const precioUnitario = precioBase * (1 - descuento);
        const total = precioUnitario * cantidad;
        
        const fila = document.createElement('tr');
        fila.innerHTML = `
            <td class="fw-bold">${cantidad.toLocaleString()}</td>
            <td>$${precioUnitario.toFixed(2)}</td>
            <td>${(descuento * 100).toFixed(0)}%</td>
            <td class="fw-bold text-success">$${total.toLocaleString()}</td>
        `;
        
        tablaBody.appendChild(fila);
    });
    
    tablaContainer.style.display = 'block';
}

// Calcular totales de la cotización
function calcularTotales() {
    let subtotal = 0;
    
    // Sumar todos los detalles visibles
    document.querySelectorAll('.detalle-form:not([style*="display: none"])').forEach(detalle => {
        const cantidadInput = detalle.querySelector('[name*="cantidad_minima"]');
        const precioInput = detalle.querySelector('[name*="precio_unitario"]');
        
        if (cantidadInput && precioInput) {
            const cantidad = parseFloat(cantidadInput.value) || 0;
            const precio = parseFloat(precioInput.value) || 0;
            subtotal += cantidad * precio;
        }
    });
    
    // Aplicar descuento
    const descuentoPorcentaje = parseFloat(document.querySelector('#id_descuento_porcentaje')?.value) || 0;
    const descuentoValor = subtotal * (descuentoPorcentaje / 100);
    const subtotalConDescuento = subtotal - descuentoValor;
    
    // Calcular IVA
    const incluirIva = document.querySelector('#id_incluir_iva')?.checked || false;
    const ivaPorcentaje = parseFloat(document.querySelector('#id_iva_porcentaje')?.value) || 19;
    const ivaValor = incluirIva ? subtotalConDescuento * (ivaPorcentaje / 100) : 0;
    
    // Total final
    const total = subtotalConDescuento + ivaValor;
    
    // Actualizar displays
    actualizarDisplayTotales(subtotal, descuentoValor, ivaValor, total);
}

// Actualizar displays de totales
function actualizarDisplayTotales(subtotal, descuento, iva, total) {
    const subtotalDisplay = document.getElementById('subtotal-display');
    const descuentoDisplay = document.getElementById('descuento-display');
    const ivaDisplay = document.getElementById('iva-display');
    const totalDisplay = document.getElementById('total-display');
    
    if (subtotalDisplay) subtotalDisplay.textContent = `$${subtotal.toLocaleString()}`;
    if (descuentoDisplay) descuentoDisplay.textContent = `$${descuento.toLocaleString()}`;
    if (ivaDisplay) ivaDisplay.textContent = `$${iva.toLocaleString()}`;
    if (totalDisplay) totalDisplay.textContent = `$${total.toLocaleString()}`;
}

// Mostrar catálogo de productos
function mostrarCatalogoProductos(boton) {
    const modal = new bootstrap.Modal(document.getElementById('catalogoModal'));
    const contenedorProductos = document.getElementById('productos-catalogo');
    
    // Cargar productos en el modal
    contenedorProductos.innerHTML = '';
    
    productos.forEach(producto => {
        const col = document.createElement('div');
        col.className = 'col-md-6 col-lg-4 mb-3';
        col.innerHTML = `
            <div class="card h-100 cursor-pointer producto-catalogo" data-producto-id="${producto.id}">
                <div class="card-body">
                    <h6 class="card-title">${producto.nombre}</h6>
                    <p class="card-text small text-muted">${producto.descripcion || ''}</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">${producto.categoria__nombre || ''}</small>
                        <strong class="text-success">$${producto.precio_base || '0'}</strong>
                    </div>
                </div>
            </div>
        `;
        
        col.addEventListener('click', function() {
            const producto_id = col.querySelector('.producto-catalogo').dataset.productoId;
            const producto = productos.find(p => p.id == producto_id);
            if (producto) {
                const inputBusqueda = boton.closest('.detalle-form').querySelector('.buscar-producto');
                seleccionarProducto(producto, inputBusqueda);
                modal.hide();
            }
        });
        
        contenedorProductos.appendChild(col);
    });
    
    modal.show();
}

// Crear cliente rápido
function crearClienteRapido() {
    // Implementar modal para crear cliente rápido
    alert('Funcionalidad de crear cliente rápido en desarrollo');
}

// Estilos CSS adicionales
const estilos = `
<style>
.cursor-pointer {
    cursor: pointer;
}

.hover-bg-light:hover {
    background-color: #f8f9fa !important;
}

.producto-catalogo:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transform: translateY(-2px);
    transition: all 0.3s ease;
}

.resultados-busqueda {
    max-height: 200px;
    overflow-y: auto;
    width: 100%;
    top: 100%;
    left: 0;
}

.tabla-precios-container {
    animation: slideDown 0.3s ease-in-out;
}

@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>
`;

// Agregar estilos al head
document.head.insertAdjacentHTML('beforeend', estilos);