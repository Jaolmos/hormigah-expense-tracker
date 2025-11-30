# Configuración de Deploy Automático con GitHub Actions

Este documento explica cómo configurar el sistema de deploy automático para Hormigah.

## Requisitos Previos

1. Servidor de producción con acceso SSH
2. Docker y Docker Compose instalados en el servidor
3. Proyecto clonado en el servidor
4. Acceso de administrador al repositorio de GitHub

## Paso 1: Generar Clave SSH (si no tienes una)

En tu servidor de producción, genera una clave SSH:

```bash
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/github_actions_deploy
```

Esto creará dos archivos:
- `~/.ssh/github_actions_deploy` (clave privada)
- `~/.ssh/github_actions_deploy.pub` (clave pública)

## Paso 2: Configurar Autenticación SSH

Agrega la clave pública al archivo authorized_keys del servidor:

```bash
cat ~/.ssh/github_actions_deploy.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

## Paso 3: Obtener la Clave Privada

Copia el contenido de la clave privada:

```bash
cat ~/.ssh/github_actions_deploy
```

Guarda este contenido completo (incluyendo las líneas `-----BEGIN OPENSSH PRIVATE KEY-----` y `-----END OPENSSH PRIVATE KEY-----`).

## Paso 4: Configurar GitHub Secrets

Ve a tu repositorio en GitHub: `Settings > Secrets and variables > Actions > New repository secret`

Crea los siguientes secrets:

### SSH_HOST
- **Nombre:** `SSH_HOST`
- **Valor:** La IP o dominio de tu servidor (ejemplo: `123.45.67.89` o `hormigah.duckdns.org`)

### SSH_USER
- **Nombre:** `SSH_USER`
- **Valor:** El usuario SSH de tu servidor (ejemplo: `jose` o `ubuntu`)

### SSH_PRIVATE_KEY
- **Nombre:** `SSH_PRIVATE_KEY`
- **Valor:** El contenido completo de la clave privada que copiaste en el Paso 3

### SSH_PORT
- **Nombre:** `SSH_PORT`
- **Valor:** El puerto SSH (normalmente `22`, pero puede ser diferente si lo has cambiado)

### PROJECT_PATH
- **Nombre:** `PROJECT_PATH`
- **Valor:** La ruta absoluta del proyecto en tu servidor
- **Ejemplo:** `/home/jose/Proyectos/Django/gastoshormigah/hormigah`

## Paso 5: Verificar Permisos del Script

En tu servidor, asegúrate de que el script de deploy sea ejecutable:

```bash
cd /ruta/de/tu/proyecto
chmod +x deploy.sh
```

## Paso 6: Probar la Conexión SSH

Desde tu máquina local, prueba la conexión con la clave privada:

```bash
ssh -i ~/.ssh/github_actions_deploy usuario@servidor -p puerto
```

Si la conexión funciona, GitHub Actions también podrá conectarse.

## Paso 7: Hacer Push a Main para Deploy Automático

Una vez configurado todo, cada push a la rama `main` ejecutará automáticamente el deploy:

```bash
git add .
git commit -m "feat: nueva funcionalidad"
git push origin main
```

## Paso 8: Deploy Manual desde GitHub

También puedes ejecutar el deploy manualmente desde GitHub:

1. Ve a `Actions` en tu repositorio
2. Selecciona el workflow "Deploy to Production"
3. Click en "Run workflow"
4. Selecciona la rama `main`
5. Click en "Run workflow"

## Verificar el Deploy

Después de cada deploy, puedes verificar:

1. **GitHub Actions:**
   - Ve a la pestaña `Actions` en GitHub
   - Verifica que el workflow completó exitosamente

2. **En el servidor:**
   ```bash
   docker-compose -f docker-compose.prod.yml ps
   docker-compose -f docker-compose.prod.yml logs --tail=50 web
   ```

3. **En el navegador:**
   - Visita tu sitio web y verifica los cambios

## Troubleshooting

### Error: Permission denied (publickey)

**Problema:** GitHub Actions no puede conectarse por SSH.

**Solución:**
1. Verifica que copiaste la clave privada completa en GitHub Secrets
2. Verifica que la clave pública está en `~/.ssh/authorized_keys`
3. Verifica los permisos: `chmod 600 ~/.ssh/authorized_keys`

### Error: docker-compose: command not found

**Problema:** Docker Compose no está instalado o no está en el PATH.

**Solución:**
```bash
# Verificar instalación
which docker-compose

# Si no está instalado, instalar Docker Compose
sudo apt-get update
sudo apt-get install docker-compose
```

### Error: No such file or directory (deploy.sh)

**Problema:** El script de deploy no existe en el servidor.

**Solución:**
```bash
cd /ruta/del/proyecto
git pull origin main
chmod +x deploy.sh
```

### Los cambios no se reflejan después del deploy

**Problema:** Docker usa la imagen cacheada antigua.

**Solución:** El script ya hace `build`, pero puedes forzar rebuild:
```bash
docker-compose -f docker-compose.prod.yml build --no-cache web
docker-compose -f docker-compose.prod.yml up -d
```

## Seguridad

1. **NUNCA** compartas tus claves SSH privadas
2. **NUNCA** hagas commit de las claves en el repositorio
3. Usa claves SSH específicas para GitHub Actions (no reutilices tu clave personal)
4. Considera usar un usuario con permisos limitados para el deploy
5. Revisa regularmente los logs de acceso SSH

## Flujo de Trabajo Recomendado

1. **Desarrollo local:** Trabaja en una rama feature
2. **Pull request:** Crea PR hacia `develop`
3. **Revisión:** Revisa y prueba los cambios
4. **Merge a develop:** Fusiona el PR
5. **Testing:** Prueba en develop
6. **Merge a main:** Cuando esté listo para producción
7. **Deploy automático:** GitHub Actions despliega automáticamente

## Comandos Útiles

### Ver logs del deploy en GitHub Actions
```
Ve a: https://github.com/TU_USUARIO/TU_REPO/actions
```

### Ver logs en el servidor
```bash
docker-compose -f docker-compose.prod.yml logs -f web
```

### Rollback manual
```bash
git log --oneline  # Ver commits
git checkout COMMIT_HASH  # Volver a un commit anterior
bash deploy.sh
```

### Reiniciar servicios manualmente
```bash
docker-compose -f docker-compose.prod.yml restart web
```
