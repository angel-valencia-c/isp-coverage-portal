/**
 * Portal Público - Formulario de Solicitud
 * Validaciones y envío de solicitud de instalación
 */

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('solicitudForm');
    const submitBtn = document.getElementById('submitBtn');
    const resultadoContainer = document.getElementById('resultado');
    
    // Validación en tiempo real del teléfono
    const telefonoInput = document.getElementById('telefono_contacto');
    telefonoInput.addEventListener('input', function(e) {
        // Solo permitir números
        this.value = this.value.replace(/[^0-9]/g, '');
        
        // Validar longitud
        if (this.value.length === 10) {
            verificarDuplicado(this.value);
        }
    });
    
    // Validación del formulario
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Limpiar errores anteriores
        limpiarErrores();
        
        // Validar campos
        if (!validarFormulario()) {
            return;
        }
        
        // Mostrar loading
        submitBtn.disabled = true;
        submitBtn.textContent = 'Enviando...';
        
        try {
            const data = {
                nombre_prospecto: document.getElementById('nombre_prospecto').value,
                telefono_contacto: document.getElementById('telefono_contacto').value,
                direccion_especifica: document.getElementById('direccion_especifica').value,
                municipio_id: parseInt(document.getElementById('municipio_id').value),
                colonia_id: parseInt(document.getElementById('colonia_id').value),
                plan_id: parseInt(document.getElementById('plan_id').value),
                costo_instalacion_cotizado: parseFloat(document.getElementById('costo_instalacion').value),
                precio_mensual_cotizado: parseFloat(document.getElementById('precio_mensual').value)
            };
            
            const response = await fetch('/api/solicitud', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Redirigir a página de confirmación
                window.location.href = `/confirmacion/${result.solicitud_id}`;
            } else {
                mostrarError(result.error);
            }
            
        } catch (error) {
            console.error('Error:', error);
            mostrarError('Error al enviar la solicitud. Por favor intenta de nuevo.');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Enviar Solicitud';
        }
    });
    
    async function verificarDuplicado(telefono) {
        try {
            const response = await fetch('/api/verificar-duplicado', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ telefono_contacto: telefono })
            });
            
            const result = await response.json();
            
            if (result.es_duplicado) {
                mostrarErrorTelefono('Ya existe una solicitud pendiente con este teléfono');
            }
        } catch (error) {
            console.error('Error al verificar duplicado:', error);
        }
    }
    
    function validarFormulario() {
        let isValid = true;
        
        // Validar nombre
        const nombre = document.getElementById('nombre_prospecto').value.trim();
        if (!nombre) {
            mostrarErrorNombre('El nombre es obligatorio');
            isValid = false;
        } else if (nombre.length < 3) {
            mostrarErrorNombre('El nombre debe tener al menos 3 caracteres');
            isValid = false;
        }
        
        // Validar teléfono
        const telefono = document.getElementById('telefono_contacto').value.trim();
        if (!telefono) {
            mostrarErrorTelefono('El teléfono es obligatorio');
            isValid = false;
        } else if (telefono.length !== 10) {
            mostrarErrorTelefono('El teléfono debe tener 10 dígitos');
            isValid = false;
        }
        
        // Validar dirección
        const direccion = document.getElementById('direccion_especifica').value.trim();
        if (!direccion) {
            mostrarErrorDireccion('La dirección es obligatoria');
            isValid = false;
        } else if (direccion.length < 10) {
            mostrarErrorDireccion('La dirección debe ser más detallada');
            isValid = false;
        }
        
        return isValid;
    }
    
    function mostrarErrorNombre(mensaje) {
        const errorSpan = document.getElementById('error-nombre');
        errorSpan.textContent = mensaje;
        errorSpan.style.display = 'block';
    }
    
    function mostrarErrorTelefono(mensaje) {
        const errorSpan = document.getElementById('error-telefono');
        errorSpan.textContent = mensaje;
        errorSpan.style.display = 'block';
    }
    
    function mostrarErrorDireccion(mensaje) {
        const errorSpan = document.getElementById('error-direccion');
        errorSpan.textContent = mensaje;
        errorSpan.style.display = 'block';
    }
    
    function mostrarError(mensaje) {
        resultadoContainer.style.display = 'block';
        resultadoContainer.className = 'resultado-container result-error';
        resultadoContainer.innerHTML = `
            <div class="result-icon">❌</div>
            <h3 class="result-title">Error</h3>
            <p class="result-message">${mensaje}</p>
        `;
        resultadoContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    
    function limpiarErrores() {
        document.getElementById('error-nombre').style.display = 'none';
        document.getElementById('error-telefono').style.display = 'none';
        document.getElementById('error-direccion').style.display = 'none';
        resultadoContainer.style.display = 'none';
    }
});
