# GitHub Secrets Configuration

Para que el deployment automático funcione, necesitas configurar estos **GitHub Secrets** en tu repositorio.

## 🔑 Cómo configurar los Secrets

1. Ve a tu repositorio en GitHub
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Agrega cada secret con su valor

## 📋 Secrets requeridos

### **Configuración del Servidor**
```
SERVER_HOST = 207.154.251.112
SERVER_USER = root
SERVER_PATH = /root/hormigah-expense-tracker
SSH_PORT = 22
```

### **Configuración SSH**
```
SSH_PRIVATE_KEY = [tu clave SSH privada completa]
```

### **Configuración Docker**
```
DOCKER_IMAGE_NAME = hormigah-expense-tracker_web
DOCKER_BACKUP_PREFIX = hormigah-backup
```

### **Configuración de Salud**
```
HEALTH_CHECK_PATH = /admin/login/
PRODUCTION_DOMAIN = https://hormigah.duckdns.org
```

### **Notificaciones (opcional)**
```
SLACK_WEBHOOK_URL = [tu webhook de Slack si quieres notificaciones]
```

## 🔐 Obtener tu clave SSH privada

En tu máquina local, ejecuta:

```bash
# Ver tu clave SSH privada
cat ~/.ssh/id_rsa

# O generar una nueva específicamente para GitHub Actions
ssh-keygen -t rsa -b 4096 -C "github-actions@hormigah" -f ~/.ssh/github_actions_key

# Agregar la clave pública al servidor
ssh-copy-id -i ~/.ssh/github_actions_key.pub root@207.154.251.112

# Usar la privada en GitHub Secrets
cat ~/.ssh/github_actions_key
```

## ✅ Lista de verificación

- [ ] SSH_PRIVATE_KEY configurado
- [ ] SERVER_* variables configuradas
- [ ] DOCKER_* variables configuradas
- [ ] PRODUCTION_DOMAIN configurado
- [ ] Clave SSH pública agregada al servidor
- [ ] Primer push a main para probar

## 🚀 Después de configurar

1. Haz push de esta rama a GitHub
2. Crea un Pull Request a `main`
3. Cuando merges, el deployment se ejecutará automáticamente
4. Revisa los logs en Actions para verificar que todo funcione

## 🔄 Proceso completo

```
1. Push to main → Tests automáticos
2. Tests pasan → Deploy automático
3. Deploy falla → Rollback automático
4. Deploy exitoso → Health checks
5. Todo bien → Notificación de éxito
```

## 📝 Valores exactos para copiar

```
SERVER_HOST: 207.154.251.112
SERVER_USER: root
SERVER_PATH: /root/hormigah-expense-tracker
SSH_PORT: 22
DOCKER_IMAGE_NAME: hormigah-expense-tracker_web
DOCKER_BACKUP_PREFIX: hormigah-backup
HEALTH_CHECK_PATH: /admin/login/
PRODUCTION_DOMAIN: https://hormigah.duckdns.org
``` 