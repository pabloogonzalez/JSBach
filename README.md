# ⚠️ JSBach — Rama `Vulnerable` (Entorno de Laboratorio de Seguridad)

> **ADVERTENCIA CRÍTICA:** Esta rama contiene vulnerabilidades de seguridad **intencionadas**. Está diseñada exclusivamente para prácticas de ciberseguridad en entornos controlados. **NUNCA debe desplegarse en producción ni en redes accesibles desde internet.**

---

## 🎯 Propósito de esta Rama

Esta rama (`Vulnerable`) contiene la versión **original del código base del profesor**, sin ningún parche de seguridad aplicado. Su único objetivo es servir como **diana de entrenamiento** para la práctica de:

- **Penetration Testing** (pruebas de intrusión)
- **Análisis de tráfico HTTP** con herramientas como Burp Suite
- **Explotación y comprensión de vulnerabilidades web** reales
- **Auditoría de código seguro** (Secure Code Review)
- **Aplicación práctica de OWASP Top 10**

La rama `main` del mismo repositorio contiene la versión modernizada y parcialmente mejorada, útil para comparar código vulnerable vs. código más seguro.

---

## 🗂️ Estructura del Proyecto

JSBach es un **sistema de administración web para un router Linux** construido íntegramente en Bash CGI sobre Apache2. Gestiona:

| Módulo | Funcionalidad |
|---|---|
| `ifwan` | Configuración de la interfaz WAN (DHCP / Manual) |
| `enrutar` | Activación del enrutamiento y NAT (MASQUERADE) |
| `bridge` | Gestión del switch virtual y VLANs 802.1Q |
| `tallafocs` | Reglas de firewall con iptables |
| `dmz` | Configuración de la zona desmilitarizada |
| `dhcp` | Servidor DHCP via dnsmasq |
| `wifi` | Punto de acceso WiFi con hostapd |
| `portal_captiu` | Portal cautivo con autenticación de usuarios |
| `vpn_wg` | Túnel VPN con WireGuard |
| `switchs` | Gestión de switches externos |
| `portmirror` | Espejado de puertos para análisis de tráfico |

```
JSBach/
├── cgi-bin/        # 65 scripts CGI (interfaz web en Bash)
├── conf/           # Ficheros de configuración (algunos con secretos)
├── scripts/        # Lógica de backend (ejecutada como root via socket)
├── system/         # Daemon jsbach_srv y gestor de socket CLI
├── install/        # Script de instalación
└── portal_captiu/  # HTML del portal cautivo
```

---

## 🔓 Vulnerabilidades Conocidas (Intencionadas)

Las siguientes vulnerabilidades han sido documentadas mediante auditoría formal y están presentes en esta rama de forma **deliberada** para su explotación controlada:

### 🔴 Críticas
| ID | Vulnerabilidad | Archivo | OWASP |
|---|---|---|---|
| V-01 | **Sin autenticación** en toda la interfaz web | `install/install` (Apache config) | A07:2021 |
| V-02 | **Claves privadas WireGuard en texto claro** en el repositorio | `conf/vpn_wg.conf` | A02:2021 |
| V-03 | **Contraseñas de usuarios en texto claro** | `conf/portal_captiu_usuaris.conf` | A02:2021 |

### 🟠 Altas
| ID | Vulnerabilidad | Archivo | OWASP |
|---|---|---|---|
| V-04 | **OS Argument Injection** vía `MODULS_EXTRA` (iptables) | `cgi-bin/tallafocs-afegir-regla.cgi` | A03:2021 |
| V-05 | **OS Argument Injection** vía `$usuari`/`$contrasenya` | `cgi-bin/validacio.cgi` | A03:2021 |
| V-06 | **Open Redirect** vía parámetro `retorn` sin validar | `cgi-bin/tallafocs-afegir-regla.cgi` | A01:2021 |
| V-07 | **Reflected XSS** en múltiples parámetros GET | `cgi-bin/tallafocs-crear-regla.cgi`, `portal_captiu.cgi` | A03:2021 |
| V-08 | **Path Traversal** en construcción de rutas con `$VNOM` | `cgi-bin/tallafocs-crear-regla.cgi` | A01:2021 |

### 🟡 Medias
| ID | Vulnerabilidad | Archivo | OWASP |
|---|---|---|---|
| V-09 | **Socket TCP sin autenticación** (127.0.0.1:1234) | `system/scr_cli` | A07:2021 |
| V-10 | **Contraseñas visibles en HTML** (tabla de usuarios) | `cgi-bin/portal_captiu-configuracio.cgi` | A02:2021 |
| V-11 | **CSRF** — toda la configuración usa método GET | Múltiples CGIs | A01:2021 |
| V-12 | **Information Disclosure** en endpoint de métricas | `cgi-bin/metricas_api.cgi` | A05:2021 |

### 🟢 Bajas
| ID | Vulnerabilidad | Archivo |
|---|---|---|
| V-13 | **Headers de seguridad HTTP ausentes** (CSP, X-Frame-Options...) | Configuración Apache |
| V-14 | **CDN sin Subresource Integrity (SRI)** | `cgi-bin/main.cgi` |

---

## 🛠️ Instalación del Entorno de Lab

> Usar únicamente en una **máquina virtual aislada** o en una red exclusivamente de laboratorio.

```bash
# 1. Clonar el repositorio en la rama Vulnerable
git clone -b Vulnerable https://github.com/tu-usuario/JSBach.git
cd JSBach

# 2. Ejecutar el script de instalación como root
cd install
sudo ./install

# 3. Acceder a la interfaz web
# http://[IP-del-router]/cgi-bin/main.cgi
```

**Requisitos del sistema:**
- Debian / Ubuntu (probado en Debian 12)
- Apache2 con mod_cgi habilitado
- Paquetes: `net-tools`, `iw`, `dnsmasq`, `hostapd`, `wireguard`

---

## 🔬 Ejercicios Propuestos

### Nivel Básico
1. **Reconocimiento sin autenticación** — Explorar toda la interfaz sin credenciales. ¿Qué información sensible encuentras sin hacer nada?
2. **Information Disclosure** — Acceder a `metricas_api.cgi` directamente. ¿Qué expone?
3. **Credenciales en texto claro** — Localiza los archivos `conf/portal_captiu_usuaris.conf` y `conf/vpn_wg.conf`. ¿Qué secretos contienen?

### Nivel Intermedio
4. **Reflected XSS** — Inyecta `<script>alert('XSS')</script>` en el parámetro `vnom` de `tallafocs-crear-regla.cgi`.
5. **Open Redirect** — Manipula el parámetro `retorn` para redirigir a una URL externa.
6. **Path Traversal** — Intenta leer `/etc/passwd` manipulando el parámetro `vnom` con `../../etc/passwd`.
7. **CSRF** — Construye una URL que active/desactive el firewall sin que el administrador lo sepa.

### Nivel Avanzado
8. **Argument Injection via MODULS_EXTRA** — Usa el campo de módulos extra del formulario de reglas de firewall para inyectar argumentos no previstos en iptables.
9. **Argument Injection vía Portal Cautivo** — Estudia cómo `validacio.cgi` pasa `$usuari` y `$contrasenya` directamente a `client_srv_cli` sin validar. ¿Puedes manipular la llamada?
10. **Escalada via Socket** — Estudia el socket TCP en `127.0.0.1:1234`. ¿Cómo lo usarías si tuvieras acceso al servidor?

---

## 🧰 Herramientas Recomendadas

| Herramienta | Uso |
|---|---|
| **Burp Suite Community** | Interceptar y modificar peticiones HTTP, fuzzing |
| **OWASP ZAP** | Análisis automático de vulnerabilidades web |
| **curl / wget** | Pruebas manuales de endpoints CGI |
| **nikto** | Escaneo básico de vulnerabilidades web |
| **gobuster / ffuf** | Descubrimiento de rutas y parámetros |
| **Wireshark** | Análisis de tráfico (HTTP en claro) |

---

## 🌿 Estructura del Repositorio (Ramas)

| Rama | Descripción |
|---|---|
| `Vulnerable` ⬅ | **Esta rama.** Versión original del profesor, con vulnerabilidades para el lab |
| `main` | Versión modernizada con Tailwind CSS, Dashboard, telemetría real |
| `v2` | Rama de desarrollo alternativa |

---

## ⚖️ Aviso Legal y Ético

Este proyecto se usa con fines **estrictamente educativos** en el contexto de un módulo de **ciberseguridad y administración de sistemas**.

- ✅ Permitido: Usar este entorno en máquinas virtuales propias o en un laboratorio de red controlado.
- ✅ Permitido: Explotar las vulnerabilidades documentadas para aprender técnicas de pentesting.
- ❌ Prohibido: Desplegar esta versión en redes de producción o accesibles desde internet.
- ❌ Prohibido: Usar las técnicas aprendidas aquí contra sistemas sin autorización explícita.

> _"Con gran poder viene una gran responsabilidad."_  
> El conocimiento de estas vulnerabilidades debe usarse para **construir sistemas más seguros**, no para atacar sistemas ajenos.

---

## 📚 Referencias

- [OWASP Top 10 (2021)](https://owasp.org/www-project-top-ten/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
