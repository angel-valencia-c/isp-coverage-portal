/**
 * Portal Público - Página de Planes
 * Funcionalidad de selección de plan y cotización
 */

let planSeleccionado = null;

document.addEventListener('DOMContentLoaded', function() {
    // Event listeners para botones de selección de plan
    document.querySelectorAll('.plan-select-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const planId = this.dataset.planId;
            const planName = this.dataset.planName;
            const costoInstalacion = parseFloat(this.dataset.costoInstalacion);
            const precioMensual = parseFloat(this.dataset.precioMensual);
            
            planSeleccionado = {
                id: planId,
                nombre: planName,
                costoInstalacion: costoInstalacion,
                precioMensual: precioMensual
            };
            
            mostrarCotizacion(planId);
        });
    });
});

async function mostrarCotizacion(planId) {
    const modal = document.getElementById('cotizacionModal');
    const detailsContainer = document.getElementById('cotizacionDetails');
    
    // Mostrar loading
    detailsContainer.innerHTML = '<div class="loading">Calculando cotización...</div>';
    modal.style.display = 'flex';
    
    try {
        // Obtener cobertura ID de la URL
        const coloniaId = window.location.pathname.split('/').pop();
        
        // Llamar a la API de cotización
        const response = await fetch(`/api/cotizacion/${coloniaId}/${planId}`);
        
        if (!response.ok) {
            throw new Error('Error al calcular cotización');
        }
        
        const cotizacion = await response.json();
        
        // Mostrar detalles de la cotización
        detailsContainer.innerHTML = `
            <div class="cotizacion-plan">
                <h4>${cotizacion.plan_nombre}</h4>
            </div>
            <div class="cotizacion-breakdown">
                <div class="cotizacion-item">
                    <span class="cotizacion-label">Costo de instalación:</span>
                    <span class="cotizacion-value">$${cotizacion.costo_instalacion.toFixed(2)}</span>
                </div>
                <div class="cotizacion-item">
                    <span class="cotizacion-label">Mensualidad:</span>
                    <span class="cotizacion-value">$${cotizacion.precio_mensual.toFixed(2)}/mes</span>
                </div>
                <div class="cotizacion-item cotizacion-total">
                    <span class="cotizacion-label">Total inicial:</span>
                    <span class="cotizacion-value">$${cotizacion.total_inicial.toFixed(2)}</span>
                </div>
            </div>
            <p class="cotizacion-note">
                El total inicial incluye el costo de instalación más el primer mes de servicio.
            </p>
        `;
        
    } catch (error) {
        console.error('Error:', error);
        detailsContainer.innerHTML = `
            <div class="error-message">
                <p>Error al calcular la cotización. Por favor intenta de nuevo.</p>
            </div>
        `;
    }
}

function cerrarModal() {
    const modal = document.getElementById('cotizacionModal');
    modal.style.display = 'none';
    planSeleccionado = null;
}

function continuarSolicitud() {
    if (!planSeleccionado) {
        alert('Por favor selecciona un plan primero');
        return;
    }
    
    // Guardar información del plan en sessionStorage para el formulario
    sessionStorage.setItem('planSeleccionado', JSON.stringify(planSeleccionado));
    
    // Redirigir al formulario de solicitud (Fase 6)
    // Por ahora, mostrar mensaje
    alert('Próximamente: Formulario de solicitud de instalación');
    
    // Cerrar modal
    cerrarModal();
}

// Cerrar modal al hacer clic fuera
window.onclick = function(event) {
    const modal = document.getElementById('cotizacionModal');
    if (event.target === modal) {
        cerrarModal();
    }
}

// Cerrar modal con tecla Escape
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        cerrarModal();
    }
});
