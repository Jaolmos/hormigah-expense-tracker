/**
 * Dashboard JavaScript - Hormigah App
 * Maneja gráficos Chart.js y funcionalidad del dashboard
 */

// Configuración global de Chart.js
Chart.defaults.font.family = 'Nunito, system-ui, sans-serif';

// Función para obtener colores según el tema actual
function getChartColors() {
    const isDark = document.documentElement.classList.contains('dark');
    return {
        textColor: isDark ? '#D1D5DB' : '#6B7280',          // gray-300 / gray-500
        gridColor: isDark ? 'rgba(75, 85, 99, 0.3)' : 'rgba(209, 213, 219, 0.5)', // gray-600 / gray-300
        borderColor: isDark ? '#374151' : '#ffffff',        // gray-700 / white
        tooltipBg: isDark ? '#1F2937' : '#ffffff',          // gray-800 / white
        tooltipBorder: isDark ? '#4B5563' : '#E5E7EB'       // gray-600 / gray-200
    };
}

// Aplicar colores iniciales
Chart.defaults.color = getChartColors().textColor;

// Event listener para auto-refresh del dashboard
document.addEventListener('DOMContentLoaded', function() {
    // Listener para recargar página después de agregar gasto en dashboard
    document.body.addEventListener('refreshDashboard', function() {
        setTimeout(function() {
            window.location.reload();
        }, 1500); // Esperar 1.5 segundos para ver el mensaje
    });
});

// Variable global para almacenar las instancias de los gráficos
let categoryChartInstance = null;
let trendChartInstance = null;

/**
 * Inicializa el gráfico de dona de categorías
 * @param {Object} data - Datos para el gráfico
 */
function initCategoryChart(data) {
    const categoryCtx = document.getElementById('categoryChart');
    if (!categoryCtx) return;

    const colors = getChartColors();

    // Destruir instancia anterior si existe
    if (categoryChartInstance) {
        categoryChartInstance.destroy();
    }

    categoryChartInstance = new Chart(categoryCtx.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: data.categories,
            datasets: [{
                data: data.amounts,
                backgroundColor: data.colors,
                borderWidth: 2,
                borderColor: colors.borderColor
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        color: colors.textColor
                    }
                },
                tooltip: {
                    backgroundColor: colors.tooltipBg,
                    borderColor: colors.tooltipBorder,
                    borderWidth: 1,
                    titleColor: colors.textColor,
                    bodyColor: colors.textColor,
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return context.label + ': €' + value.toLocaleString() + ' (' + percentage + '%)';
                        }
                    }
                }
            }
        }
    });
}

/**
 * Inicializa el gráfico de líneas de tendencia
 * @param {Object} data - Datos para el gráfico
 */
function initTrendChart(data) {
    const trendCtx = document.getElementById('trendChart');
    if (!trendCtx) return;

    const colors = getChartColors();

    // Destruir instancia anterior si existe
    if (trendChartInstance) {
        trendChartInstance.destroy();
    }

    trendChartInstance = new Chart(trendCtx.getContext('2d'), {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [{
                label: 'Gastos Diarios',
                data: data.amounts,
                borderColor: '#3B82F6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#3B82F6',
                pointBorderColor: colors.borderColor,
                pointBorderWidth: 2,
                pointRadius: 6,
                pointHoverRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: colors.tooltipBg,
                    borderColor: colors.tooltipBorder,
                    borderWidth: 1,
                    titleColor: colors.textColor,
                    bodyColor: colors.textColor,
                    callbacks: {
                        label: function(context) {
                            return 'Gasto: €' + context.parsed.y.toLocaleString();
                        }
                    }
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Fecha',
                        color: colors.textColor
                    },
                    ticks: {
                        maxTicksLimit: 10,
                        color: colors.textColor
                    },
                    grid: {
                        color: colors.gridColor
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Monto (€)',
                        color: colors.textColor
                    },
                    ticks: {
                        color: colors.textColor,
                        callback: function(value) {
                            return '€' + value.toLocaleString();
                        }
                    },
                    grid: {
                        color: colors.gridColor
                    }
                }
            }
        }
    });
}

// Variable global para almacenar los datos de los gráficos
let currentChartData = null;

/**
 * Inicializa todos los gráficos del dashboard
 * @param {Object} chartData - Todos los datos de gráficos
 */
function initDashboardCharts(chartData) {
    // Guardar datos para poder reinicializar en cambio de tema
    currentChartData = chartData;

    // Inicializar gráfico de categorías si hay datos
    if (chartData.categories && chartData.categories.length > 0) {
        initCategoryChart({
            categories: chartData.categories,
            amounts: chartData.amounts,
            colors: chartData.colors
        });
    }

    // Inicializar gráfico de tendencia si hay datos
    if (chartData.dates && chartData.dates.length > 0) {
        initTrendChart({
            dates: chartData.dates,
            amounts: chartData.dailyAmounts
        });
    }
}

// Listener para cambio de tema - reinicializar gráficos
window.addEventListener('themeChanged', function() {
    // Actualizar color global de Chart.js
    Chart.defaults.color = getChartColors().textColor;

    // Reinicializar gráficos con los datos actuales
    if (currentChartData) {
        initDashboardCharts(currentChartData);
    }
}); 