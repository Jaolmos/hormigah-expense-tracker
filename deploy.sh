#!/bin/bash

# Script de deploy para Hormigah
# Este script se ejecuta en el servidor de producción

set -e  # Detener en caso de error

echo "=== Iniciando deploy de Hormigah ==="
echo "Fecha: $(date)"

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 1. Pull de los últimos cambios (ya hecho por GitHub Actions, pero por si acaso)
print_message "Verificando últimos cambios de Git..."
git pull origin main

# 2. Detener servicios
print_message "Deteniendo contenedores..."
docker-compose -f docker-compose.prod.yml down

# 3. Rebuild de la imagen web (para incluir cambios en templates/código)
print_message "Reconstruyendo imagen web..."
docker-compose -f docker-compose.prod.yml build web

# 4. Iniciar servicios
print_message "Iniciando contenedores..."
docker-compose -f docker-compose.prod.yml up -d

# 5. Esperar a que los servicios estén listos
print_message "Esperando a que los servicios estén listos..."
sleep 10

# 6. Ejecutar migraciones (si las hay)
print_message "Ejecutando migraciones de base de datos..."
docker-compose -f docker-compose.prod.yml exec -T web python manage.py migrate --noinput

# 7. Collectstatic
print_message "Recolectando archivos estáticos..."
docker-compose -f docker-compose.prod.yml exec -T web python manage.py collectstatic --noinput

# 8. Verificar estado de los contenedores
print_message "Verificando estado de los contenedores..."
docker-compose -f docker-compose.prod.yml ps

# 9. Verificar logs recientes
print_message "Últimas líneas de logs:"
docker-compose -f docker-compose.prod.yml logs --tail=20 web

echo ""
print_message "Deploy completado exitosamente!"
echo "=== Fin del deploy ==="
