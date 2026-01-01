// frontend/app.js

const API_URL = 'http://localhost:5001/api';

// Cargar recetas al iniciar
async function cargarRecetas() {
    const select = document.getElementById('receta');
    const resultadoDiv = document.getElementById('resultado');
    
    try {
        const response = await fetch(`${API_URL}/recipes`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (!data.recipes || data.recipes.length === 0) {
            resultadoDiv.innerHTML = '<p class="error">No se encontraron recetas</p>';
            return;
        }
        
        // Limpiar opciones anteriores
        select.innerHTML = '';
        
        // Agregar opción por defecto
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = '-- Seleccione una receta --';
        select.appendChild(defaultOption);
        
        data.recipes.forEach(receta => {
            const option = document.createElement('option');
            option.value = receta.nombre;
            option.textContent = receta.nombre;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error cargando recetas:', error);
        resultadoDiv.innerHTML = `<p class="error">Error cargando recetas: ${error.message}. Verifica que la API esté corriendo en ${API_URL}</p>`;
    }
}

// Calcular costo
async function calcularCosto() {
    const receta = document.getElementById('receta').value;
    const fecha = document.getElementById('fecha').value;
    const resultadoDiv = document.getElementById('resultado');
    
    if (!receta || !fecha) {
        resultadoDiv.innerHTML = '<p class="error">Por favor complete todos los campos</p>';
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/calculate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ recipe_name: receta, date: fecha })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            resultadoDiv.innerHTML = `
                <h2>Resultado</h2>
                <p><strong>Receta:</strong> ${data.recipe_name}</p>
                <p><strong>Fecha:</strong> ${data.calculation_date}</p>
                <p><strong>Tipo de cambio USD/ARS:</strong> ${data.exchange_rate_usd_to_ars.toFixed(2)}</p>
                <p><strong>Costo en ARS:</strong> $${data.cost_details.total_cost_ars.toFixed(2)}</p>
                <p><strong>Costo en USD:</strong> $${data.cost_details.total_cost_usd.toFixed(2)}</p>
            `;
        } else {
            resultadoDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
        }
    } catch (error) {
        resultadoDiv.innerHTML = `<p class="error">Error al calcular: ${error.message}</p>`;
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', cargarRecetas);
document.getElementById('calcular').addEventListener('click', calcularCosto);