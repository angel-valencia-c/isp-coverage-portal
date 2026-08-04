/**
 * Portal Público - JavaScript
 * Funcionalidad de búsqueda de cobertura con autocompletado
 */

document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const municipioSelect = document.getElementById('municipio');
    const coloniaSearchInput = document.getElementById('colonia-search');
    const coloniaHiddenInput = document.getElementById('colonia');
    const suggestionsDropdown = document.getElementById('colonia-suggestions');
    const resultContainer = document.getElementById('result');
    
    let searchTimeout = null;
    let selectedColonia = null;
    
    // Cargar colonias cuando se selecciona un municipio
    municipioSelect.addEventListener('change', async function() {
        const municipioId = this.value;
        
        // Limpiar selección de colonia
        coloniaSearchInput.value = '';
        coloniaHiddenInput.value = '';
        selectedColonia = null;
        suggestionsDropdown.classList.remove('active');
        resultContainer.style.display = 'none';
        
        if (!municipioId) return;
        
        // Mostrar loading
        coloniaSearchInput.classList.add('loading');
        
        try {
            const response = await fetch(`/api/colonias/${municipioId}`);
            const colonias = await response.json();
            
            // Guardar colonias para búsqueda local
            window.coloniasCache = colonias;
        } catch (error) {
            console.error('Error al cargar colonias:', error);
            alert('Error al cargar las colonias. Por favor intenta de nuevo.');
        } finally {
            coloniaSearchInput.classList.remove('loading');
        }
    });
    
    // Búsqueda con autocompletado
    coloniaSearchInput.addEventListener('input', function() {
        const termino = this.value.trim();
        
        if (termino.length < 2) {
            suggestionsDropdown.classList.remove('active');
            return;
        }
        
        // Limpiar timeout anterior
        if (searchTimeout) {
            clearTimeout(searchTimeout);
        }
        
        // Buscar con debounce
        searchTimeout = setTimeout(() => {
            buscarColonias(termino);
        }, 300);
    });
    
    // Función de búsqueda
    async function buscarColonias(termino) {
        const municipioId = municipioSelect.value;
        
        if (!municipioId) {
            alert('Por favor selecciona un municipio primero');
            return;
        }
        
        try {
            // Buscar en cache local primero
            if (window.coloniasCache) {
                const resultados = window.coloniasCache.filter(c => 
                    c.nombre.toLowerCase().includes(termino.toLowerCase())
                ).slice(0, 10);
                
                mostrarSugerencias(resultados);
            } else {
                // Si no hay cache, buscar en API
                const response = await fetch(`/api/buscar-colonias?q=${termino}&limite=10`);
                const colonias = await response.json();
                mostrarSugerencias(colonias);
            }
        } catch (error) {
            console.error('Error al buscar colonias:', error);
        }
    }
    
    // Mostrar sugerencias
    function mostrarSugerencias(colonias) {
        if (colonias.length === 0) {
            suggestionsDropdown.innerHTML = '<div class="suggestion-item">No se encontraron resultados</div>';
            suggestionsDropdown.classList.add('active');
            return;
        }
        
        suggestionsDropdown.innerHTML = colonias.map(colonia => `
            <div class="suggestion-item" data-id="${colonia.id}" data-nombre="${colonia.nombre}">
                <div class="suggestion-item-name">${colonia.nombre}</div>
                <div class="suggestion-item-municipio">${colonia.tipo}</div>
            </div>
        `).join('');
        
        suggestionsDropdown.classList.add('active');
        
        // Agregar event listeners a las sugerencias
        document.querySelectorAll('.suggestion-item').forEach(item => {
            item.addEventListener('click', function() {
                const id = this.dataset.id;
                const nombre = this.dataset.nombre;
                
                coloniaSearchInput.value = nombre;
                coloniaHiddenInput.value = id;
                selectedColonia = { id, nombre };
                suggestionsDropdown.classList.remove('active');
            });
        });
    }
    
    // Cerrar sugerencias al hacer clic fuera
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.search-input-wrapper')) {
            suggestionsDropdown.classList.remove('active');
        }
    });
    
    // Manejar envío del formulario
    searchForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const coloniaId = coloniaHiddenInput.value;
        
        if (!coloniaId) {
            alert('Por favor selecciona una colonia de la lista');
            return;
        }
        
        // Mostrar loading
        const submitBtn = searchForm.querySelector('button[type="submit"]');
        submitBtn.classList.add('btn-loading');
        submitBtn.disabled = true;
        resultContainer.style.display = 'none';
        
        try {
            const response = await fetch(`/api/verificar-cobertura/${coloniaId}`);
            const data = await response.json();
            
            mostrarResultado(data);
        } catch (error) {
            console.error('Error al verificar cobertura:', error);
            alert('Error al verificar la cobertura. Por favor intenta de nuevo.');
        } finally {
            submitBtn.classList.remove('btn-loading');
            submitBtn.disabled = false;
        }
    });
    
    // Mostrar resultado
    function mostrarResultado(data) {
        resultContainer.style.display = 'block';
        
        if (data.tiene_cobertura) {
            resultContainer.className = 'result-container result-success';
            resultContainer.innerHTML = `
                <div class="result-icon">✅</div>
                <h3 class="result-title">¡Excelentes noticias!</h3>
                <p class="result-message">Tu zona tiene cobertura disponible</p>
                <div class="result-details">
                    <div class="result-detail-item">
                        <span class="result-detail-label">Colonia:</span>
                        <span class="result-detail-value">${data.colonia.nombre}</span>
                    </div>
                    <div class="result-detail-item">
                        <span class="result-detail-label">Municipio:</span>
                        <span class="result-detail-value">${data.colonia.municipio}</span>
                    </div>
                </div>
                <p style="margin-top: var(--space-4); color: var(--color-text-secondary);">
                    Próximamente podrás ver los planes disponibles y solicitar tu instalación.
                </p>
            `;
        } else {
            resultContainer.className = 'result-container result-error';
            resultContainer.innerHTML = `
                <div class="result-icon">❌</div>
                <h3 class="result-title">Sin cobertura disponible</h3>
                <p class="result-message">Lo sentimos, tu zona aún no tiene cobertura</p>
                <div class="result-details">
                    <div class="result-detail-item">
                        <span class="result-detail-label">Colonia:</span>
                        <span class="result-detail-value">${data.colonia.nombre}</span>
                    </div>
                    <div class="result-detail-item">
                        <span class="result-detail-label">Municipio:</span>
                        <span class="result-detail-value">${data.colonia.municipio}</span>
                    </div>
                </div>
                <p style="margin-top: var(--space-4); color: var(--color-text-secondary);">
                    Estamos trabajando para llevar internet de alta velocidad a tu zona.
                    <br>Próximamente podrás dejar tus datos para ser notificado cuando haya cobertura.
                </p>
            `;
        }
        
        // Scroll al resultado
        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
});
