# Hormigah - Control Inteligente de Gastos Hormiga

Una aplicación web moderna para controlar esos pequeños gastos diarios que pasan desapercibidos pero que al final del año suman cantidades importantes. Incluye sistema de automatización con n8n para reportes mensuales inteligentes con IA.

![Django](https://img.shields.io/badge/Django-5.2.3-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django%20REST-Framework-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![HTMX](https://img.shields.io/badge/HTMX-1.9-336791?style=for-the-badge&logo=htmx&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind-3.4-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-4.4-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)
![n8n](https://img.shields.io/badge/n8n-Automation-EA4B71?style=for-the-badge&logo=n8n&logoColor=white)

## Concepto: Gastos Hormiga

Los **gastos hormiga** son pequeños desembolsos cotidianos que individualmente parecen insignificantes, pero acumulados representan una parte considerable del presupuesto:

- Café diario: €2,50 × 365 días = €912 al año
- Delivery impulsivo: €12 × 2 veces/semana = €1,248 al año  
- Taxis innecesarios: €7 × 3 veces/semana = €1,092 al año
- Suscripciones no usadas: €9 × 12 meses = €108 al año

**Total: €3,360 al año en gastos "pequeños"**

## Screenshots

### Dashboard Principal
La vista principal con métricas en tiempo real, gráficos interactivos y lista de gastos recientes.

![Dashboard Principal](screenshots/desktop/dashboard-complete-desktop.png)

### Gestión de Gastos
Lista completa de gastos con filtros avanzados y funcionalidad CRUD completa.

![Lista de Gastos](screenshots/desktop/expense-list-desktop.png)

### Modales Interactivos (HTMX)
Formularios dinámicos que se abren sin recargar la página.

| Agregar Gasto | Editar Gasto |
|---------------|--------------|
| ![Agregar Gasto](screenshots/desktop/add-expense-modal-desktop.png) | ![Editar Gasto](screenshots/desktop/edit-expense-modal-desktop.png) |

### Perfil de Usuario
Configuración personal y alertas automáticas para reportes mensuales.

![Perfil de Usuario](screenshots/desktop/user-profile-desktop.png)

### Funcionalidades Clave

#### Acceso y Autenticación
Página de login con diseño limpio y profesional.

![Login](screenshots/desktop/login-desktop.png)

#### Gestión de Presupuesto
Modal para configurar presupuesto mensual y alertas automáticas.

![Presupuesto](screenshots/desktop/budget-modal-desktop.png)

#### Diseño Responsive
La aplicación se adapta perfectamente a dispositivos móviles con navegación optimizada y formularios táctiles.

#### Filtros Avanzados
Sistema de filtros inteligentes por período, categoría y monto.

![Filtros Activos](screenshots/desktop/expense-filters-active-desktop.png)

### Versión Mobile

La aplicación cuenta con un diseño completamente responsive que se adapta perfectamente a dispositivos móviles.

#### Interfaz Principal Mobile
Dashboard optimizado para pantallas pequeñas con navegación intuitiva.

<img src="screenshots/mobile/dashboard-mobile.png" alt="Dashboard Mobile" width="300">

#### Navegación Mobile
Menú hamburguesa con acceso rápido a todas las funcionalidades.

<img src="screenshots/mobile/mobile-menu.png" alt="Mobile Menu" width="300">

#### Acceso Mobile
Página de login optimizada para dispositivos táctiles.

<img src="screenshots/mobile/login-mobile.png" alt="Login Mobile" width="300">

#### Gestión de Gastos Mobile
Lista de gastos y formularios adaptados para móviles.

<table>
<tr>
<td><strong>Lista de Gastos</strong></td>
<td><strong>Agregar Gasto</strong></td>
</tr>
<tr>
<td><img src="screenshots/mobile/expense-list-mobile.png" alt="Expense List Mobile" width="300"></td>
<td><img src="screenshots/mobile/add-expense-mobile.png" alt="Add Expense Mobile" width="300"></td>
</tr>
</table>

#### Configuración Mobile
Perfil de usuario y configuraciones optimizadas para móvil.

<img src="screenshots/mobile/user-profile-mobile.png" alt="User Profile Mobile" width="300">

## Características Principales

### Dashboard Inteligente
- Métricas en tiempo real con filtros por período
- Gráficos interactivos (dona y líneas) con Chart.js
- Auto-actualización sin recargar página (HTMX)
- Diseño responsive optimizado para móviles

### Análisis Visual
- Distribución por categorías con colores personalizados
- Tendencias temporales para identificar patrones
- Proyecciones anuales automáticas
- Comparativas mensuales

### Experiencia de Usuario
- Interfaz HTMX sin recargas de página
- Modales dinámicos para operaciones CRUD
- Auto-refresh en listas y métricas
- Navegación fluida entre secciones

### Funcionalidades Avanzadas
- Filtros inteligentes por fecha, categoría y monto
- CRUD completo con validación en tiempo real
- Sistema de categorías con colores personalizados
- Gestión de usuarios con autenticación segura
- Sistema de alertas de presupuesto automatizado
- **API REST**: Endpoints específicos para integración con n8n
- **Reportes Automatizados**: Generación mensual de reportes con IA
- **Webhooks**: Sistema de notificaciones automáticas

## Tecnologías

### Backend
- **Django 5.2.3**: Framework web robusto
- **Django REST Framework**: API REST para integración con n8n
- **PostgreSQL**: Base de datos para desarrollo y producción
- **Python 3.12**: Lenguaje base
- **Gunicorn**: Servidor WSGI para producción

### Frontend
- **HTMX**: Interactividad sin JavaScript complejo
- **Tailwind CSS**: Framework de utilidades CSS
- **Chart.js**: Gráficos interactivos
- **Alpine.js**: Interactividad ligera

### Infraestructura
- **Docker**: Containerización completa
- **Nginx**: Servidor web y proxy inverso
- **n8n**: Automatización de workflows y reportes mensuales con IA

## Instalación

### Requisitos Previos
- Docker y Docker Compose
- Git

### Setup Rápido
```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/hormigah.git
cd hormigah

# Configurar variables de entorno
cp .env.example .env.local

# Iniciar aplicación
docker-compose up -d

# Configurar Django
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# Crear categorías predeterminadas (8 categorías base)
docker-compose exec web python manage.py create_default_categories
```

### Acceso
- **Aplicación principal**: http://localhost:8000/
- **Panel de administración**: http://localhost:8000/admin/

## Estructura del Proyecto

```
hormigah/
├── apps/
│   ├── core/                     # Utilidades base y templates
│   ├── expenses/                 # App principal de gastos
│   │   ├── api/                 # API REST para n8n
│   │   │   ├── authentication.py # Bearer token auth
│   │   │   ├── serializers.py   # DRF serializers
│   │   │   ├── views.py         # API views
│   │   │   └── urls.py          # API endpoints
│   │   ├── models.py            # Category, Expense, Budget
│   │   ├── views.py             # Lógica de negocio web
│   │   ├── forms.py             # Formularios con validación
│   │   ├── utils/               # Utilidades modularizadas
│   │   ├── templates/           # Templates especializados
│   │   └── static/              # CSS y JS específicos
│   └── users/                   # Gestión de usuarios
├── config/                      # Configuración Django
│   ├── settings/                # Settings modulares
│   │   ├── base.py             # Configuración base + API REST
│   │   ├── local.py            # Desarrollo
│   │   └── production.py       # Producción
│   └── urls.py                 # URLs principales + API
├── static/                      # Archivos estáticos globales
├── docker-compose.yml           # Docker desarrollo
├── docker-compose.prod.yml      # Docker producción + n8n
├── Dockerfile                   # Imagen de la aplicación
└── requirements.txt             # Dependencias Python + DRF
```

## Uso de la Aplicación

### Dashboard Principal
- Métricas del período seleccionado
- Gráfico de distribución por categorías  
- Tendencia temporal de gastos
- Lista de gastos recientes

### Gestión de Gastos
- Agregar nuevo gasto (modal HTMX)
- Editar gasto existente (modal HTMX)
- Eliminar gasto (confirmación)
- Ver detalles completos

### Filtros Avanzados
- Por período (Este mes, último mes, últimos 7/30 días)
- Por categoría (Café, Delivery, Transporte, etc.)
- Por rango de fechas personalizado
- Por rango de montos (min/max)

### Sistema de Alertas y Reportes
- Alertas automáticas al alcanzar el 90% del presupuesto mensual
- Configuración por usuario (activar/desactivar)
- **Reportes Mensuales Automatizados**: n8n + OpenAI + Gmail
- **API REST**: Integración específica para n8n
- **Análisis Inteligente**: IA personalizada por usuario y período

## Comandos Útiles

### Desarrollo
```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f web

# Ejecutar migraciones
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Ejecutar tests
docker-compose exec web python manage.py test

# Acceder a Django shell
docker-compose exec web python manage.py shell
```

### Producción con n8n
```bash
# Desplegar aplicación + n8n
docker-compose -f docker-compose.prod.yml up -d

# Ver estado de todos los servicios
docker-compose -f docker-compose.prod.yml ps

# Ver logs específicos
docker-compose -f docker-compose.prod.yml logs web
docker-compose -f docker-compose.prod.yml logs n8n

# Acceder a n8n
# http://tu-dominio.com:5678
```

### API Testing
```bash
# Test endpoint usuarios activos
curl -H "Authorization: Bearer {token}" http://localhost:8000/api/users/active/

# Test endpoint usuario completo  
curl -H "Authorization: Bearer {token}" http://localhost:8000/api/users/1/complete/

# Verificar documentación API
curl http://localhost:8000/api/docs/
```

## API REST (Django REST Framework)

La aplicación incluye **2 endpoints específicos** desarrollados con Django REST Framework para que n8n pueda generar reportes automáticos.

### Endpoints Disponibles

#### Listar Usuarios Activos
```
GET /api/users/active/
Authorization: Bearer {N8N_API_TOKEN}
```

**Propósito**: Obtener lista de usuarios elegibles para reportes automáticos

**Retorna usuarios que**:
- Tienen presupuesto configurado
- Tienen alertas por email activadas  
- Han registrado gastos en los últimos 30 días

#### Obtener Datos Completos de Usuario
```
GET /api/users/{id}/complete/
Authorization: Bearer {N8N_API_TOKEN}
```

**Propósito**: Obtener todos los datos necesarios para generar reportes con IA

**Retorna datos completos incluyendo**:
- Información del usuario y presupuesto
- Historial completo de gastos
- Resúmenes mensuales y por categorías
- Estadísticas y tendencias

#### Documentación Interactiva
- **Swagger UI**: http://localhost:8000/api/docs/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

### Autenticación API
- **Desarrollo**: Token fijo en settings
- **Producción**: Token seguro via variables de entorno
- **Tipo**: Bearer Token personalizado

## Automatización con n8n

### Workflows Automatizados

El sistema incluye dos workflows principales de n8n para automatización completa:

![Workflow de Reportes n8n](screenshots/n8n/reports-n8n.png)

#### 1. **Reportes Mensuales Automatizados**
- **Schedule Trigger**: Se ejecuta automáticamente el día 1 de cada mes a las 9:00 AM
- **Detección de Usuarios**: Consume endpoint `/api/users/active/` para obtener usuarios elegibles
- **Análisis Individual**: Para cada usuario consume `/api/users/{id}/complete/` para obtener datos completos
- **Filtrado Temporal**: Procesa únicamente los gastos del mes anterior
- **Análisis con IA**: GPT-3.5-turbo genera reporte personalizado
- **Envío por Email**: Gmail con diseño HTML profesional

#### 2. **Alertas de Presupuesto (90%)**
- **Webhook Trigger**: Activado cuando Django detecta que un usuario supera el 90% del presupuesto
- **Procesamiento Inmediato**: Recibe datos del usuario y presupuesto actual
- **Envío de Alerta**: Email inmediato via Gmail notificando el límite alcanzado
- **Prevención de Gastos**: Ayuda a evitar superar el presupuesto mensual

### Características del Sistema IA

- **Análisis Temporal Preciso**: Solo analiza el mes anterior, no el actual
- **Métricas Financieras**: Total gastado, porcentaje del presupuesto usado
- **Desglose por Categorías**: Análisis detallado de cada tipo de gasto
- **Recomendaciones Personalizadas**: Sugerencias específicas del usuario
- **Alertas en Tiempo Real**: Notificaciones automáticas al alcanzar límites
- **Diseño Profesional**: Emails HTML con identidad visual corporativa

### Funcionalidades Destacadas
- **Auto-Refresh Inteligente**: Las listas se actualizan automáticamente
- **Interfaz Moderna**: Modales HTMX sin cambiar de página
- **Responsive Design**: Optimizado para todos los dispositivos
- **Sistema de Automatización Completo**: n8n + API REST + IA
- **Reportes Mensuales Automatizados**: Análisis personalizado con GPT
- **Integración Gmail**: Emails HTML profesionales automáticos