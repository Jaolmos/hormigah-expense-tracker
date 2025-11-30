# GitHub Actions - Hormigah

Este directorio contiene los workflows de GitHub Actions para automatizar el deploy de Hormigah.

## Workflows Disponibles

### Deploy to Production
**Archivo:** `.github/workflows/deploy-production.yml`

**Trigger:**
- Push a la rama `main`
- Ejecución manual desde GitHub Actions

**Funcionalidad:**
1. Se conecta al servidor vía SSH
2. Hace pull de los últimos cambios
3. Ejecuta el script `deploy.sh` que:
   - Reconstruye la imagen Docker
   - Reinicia los contenedores
   - Ejecuta migraciones
   - Recolecta archivos estáticos
   - Verifica el estado de los servicios

## Configuración Inicial

Sigue la guía completa en [DEPLOY_SETUP.md](./DEPLOY_SETUP.md)

**Resumen de secrets requeridos:**
- `SSH_HOST`: IP o dominio del servidor
- `SSH_USER`: Usuario SSH
- `SSH_PRIVATE_KEY`: Clave SSH privada
- `SSH_PORT`: Puerto SSH (normalmente 22)
- `PROJECT_PATH`: Ruta absoluta del proyecto en el servidor

## Uso

### Deploy Automático
Simplemente haz push a `main`:
```bash
git push origin main
```

### Deploy Manual
1. Ve a la pestaña `Actions` en GitHub
2. Selecciona "Deploy to Production"
3. Click en "Run workflow"
4. Selecciona la rama y ejecuta

## Verificación

Después de cada deploy, verifica en GitHub Actions que el workflow completó exitosamente.

En caso de error, revisa los logs en:
- GitHub: Pestaña `Actions` > Último workflow
- Servidor: `docker-compose -f docker-compose.prod.yml logs --tail=100 web`

## Documentación Adicional

- [DEPLOY_SETUP.md](./DEPLOY_SETUP.md) - Guía completa de configuración
- [deploy.sh](../deploy.sh) - Script de deploy ejecutado en el servidor
