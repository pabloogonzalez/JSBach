# JSBach - Product Requirements Document (PRD)

## 1. Introducción y Propósito
**JSBach** es un sistema de gestión y configuración de red basado en scripts de Bash desarrollados para operar en un entorno Linux. Su propósito principal es convertir un dispositivo o servidor Linux en un router/firewall de altas prestaciones, permitiendo la gestión modular de interfaces WAN, configuración de switches lógicos (bridges y VLANs), enrutamiento (NAT), reglas de cortafuegos (iptables/ebtables) y zonas desmilitarizadas (DMZ).

Este documento describe la arquitectura de los directorios clave (`conf`, `scripts`, `system`, `install`, y `cgi-bin`), las variables asociadas, la funcionalidad de cada módulo, la automatización en segundo plano y los casos de uso principales.

## 2. Estructura de Configuración (`conf/`)

El directorio `conf` almacena el estado y las variables de configuración del sistema de forma persistente.

*   `variables.conf`: Archivo principal que define las rutas absolutas (`DIR`, `PROJECTE`, `DIR_CONF`, `DIR_SCRIPTS`), nombres de archivos de configuración secundarios y estados estándar (`ACTIVAT`, `DESACTIVAT`).
*   `ifwan.conf`: Almacena la configuración de la interfaz WAN (modo `dhcp` o `manual`, dispositivo asociado, IP, máscara, puerta de enlace y servidor DNS).
*   `bridge.conf`: Define las VLANs lógicas del sistema (VLAN ID, Identificador, IP y Máscara). Siempre contempla una `vlan_Admin` (ID 1, para administración) y `vlan_DMZ` (ID 2, para servidores expuestos).
*   `bridge_if.conf`: Define la asociación de puertos de red físicos con el bridge principal (`br0`). Permite configurar qué interfaces reciben tráfico *untagged* (PVID) y *tagged* (truncado de VLANs).
*   `dmz.conf`: Contiene las reglas de redirección de puertos (Port Forwarding), indicando el puerto externo, protocolo (TCP/UDP) y la IP de destino del servidor alojado en la DMZ.
*   `ip_wls.conf` y `ports_wls.conf`: (Configuración del firewall auxiliar). Guardan qué direcciones IP / rangos MAC tienen privilegios para saltarse bloqueos e interactuar con ciertos puertos permitidos.

## 3. Funcionalidad de los Scripts (`scripts/`)

El directorio `scripts` contiene el motor central del sistema. Cada script actúa como un servicio con soporte para comandos como `iniciar`, `aturar`, `estat` (que devuelve código HTML/texto de estado) y `configurar`.

### 3.1. WAN (`ifwan`)
*   **Propósito:** Gestionar la interfaz conectada a Internet.
*   **Funcionamiento:** Capaz de levantar la interfaz utilizando un cliente DHCP (`dhcpcd`) o configurando parámetros de red estáticos (IP, máscara, gateway, modificando `systemd-resolved` para DNS). 

### 3.2. Enrutamiento (`enrutar`)
*   **Propósito:** Proveer acceso a Internet a las redes locales.
*   **Funcionamiento:** Habilita el reenvío de paquetes en el kernel de Linux (`ip_forward = 1`) y configura las reglas de SNAT (`MASQUERADE`) en `iptables` a través de la interfaz configurada como WAN. Require que `ifwan` esté previamente levantado.

### 3.3. Conmutador y VLANs (`bridge`)
*   **Propósito:** Unir interfaces físicas no utilizadas y crear la topología local de conmutador (Switch).
*   **Funcionamiento:** 
    1. Crea un dispositivo de puente virtual (`br0`) habilitado para el filtrado VLAN.
    2. Lee `bridge.conf` para instanciar subinterfaces VLAN (ej. `br0.1`, `br0.2`) asignándoles sus respectivas direcciones IP.
    3. Lee `bridge_if.conf` y añade las interfaces físicas al bridge (`br0`), asignando qué etiquetas VLAN se deben procesar por cada puerto de red físico.

### 3.4. Cortafuegos (`tallafocs`)
*   **Propósito:** Aplicar seguridad lógica, segmentar todo el tráfico y proporcionar control de acceso perimetral e interno.
*   **Funcionamiento:** 
    *   **Subcadenas por VLAN:** Implementa separación lógica granularizando mediante subcadenas como `IN_ADMIN`, `IN_DMZ`, `IN_USERS` e interceptando el tráfico desde esas VLANs específicas.
    *   **Aislamiento:** Emplea una cadena lógica `aislar` para prohibir comunicaciones indeseadas o separar clientes de diferentes VLANs.
    *   **Excepciones:** Mantiene listas blancas temporales gestionadas a través de `ports_wls` e `ip_wls` (IP/MAC checking).
    *   **Estatus:** Cuenta con un completo mecanismo HTML para reportar los niveles de acceso de cada red, qué cadenas de bloqueo (DROP) aplican a qué redes, además del estado individual de Ebtables para la capa L2.

### 3.5. DMZ (`dmz`)
*   **Propósito:** Proveer externalización de servicios alojados dentro de la infraestructura local.
*   **Funcionamiento:** Carga la configuración WAN para obtener el origen del tráfico, lee las directivas de `dmz.conf` e inyecta dinámicamente o remueve reglas en la cadena `PREROUTING` de `iptables` realizando DNAT explícito.

---

## 4. Servicios del Sistema y Automatización (`system/`)

El directorio `system` contiene los demonios y procesos en segundo plano que permiten la ejecución asíncrona de comandos y el inicio del sistema.

*   `jsbach_srv`: Script principal de arranque del servicio. Inicializa la configuración local e invoca el proceso servidor de CLI (`srv_cli`).
*   `srv_cli`: Crea una tubería con nombre (`mkfifo /tmp/f`) y levanta un listener TCP usando netcat (`nc -lk 127.0.0.1 1234`), enviando todo el tráfico entrante hacia `scr_cli`.
*   `scr_cli`: Lector del socket. Procesa las cadenas recibidas por el puerto 1234, determina el comando principal (`ifwan`, `enrutar`, `bridge`, `tallafocs`, `dmz`, `switchs`) y ejecuta el script correspondiente dentro del directorio `scripts`, pasando los argumentos necesarios. Proporciona una interfaz segura y desacoplada para los scripts CGI.

---

## 5. Interfaz Web de Gestión (`cgi-bin/`)

El directorio `cgi-bin` aloja los scripts CGI (Common Gateway Interface) desarrollados en Bash que construuyen la interfaz web del router. Estos scripts se ejecutan bajo el servidor Apache2 y actúan como puente visual ('frontend') para leer configuraciones e interactuar con el 'backend' (directorio `scripts`).

**Características Principales:**
*   **Estructura Modular:** Cada recurso del router tiene múltiples scripts asociados separados por acción: visualización (`*.cgi`), menús laterales (`*-menu.cgi`), formularios de configuración (`*-configurar.cgi`), y guardado de datos (`*-guardar.cgi`).
*   **Pantallas Principales:** 
    *   `main.cgi` / `index-admin.cgi`: Dashboard principal y panel de control general.
    *   `ifwan.cgi`: Formulario para modificar IP, máscara y DNS de la WAN o forzar DHCP.
    *   `enrutar.cgi`: Control de activación del NAT y estado actual.
    *   `bridge.cgi`: Administración de VLANs y el mapa de asociación de puertos (VLAN Tagging / Untagging).
    *   `tallafocs.cgi`: Tableros de estado del cortafuegos, bloqueos/desconexiones aisladas de VLANs e inserción de excepciones (Puertos e IPs permitidos limitadamente).
    *   `dmz.cgi`: Gestión de reenvío de puertos.
    *   `ebtables.cgi`: Refactorización de UI para aislamientos a nivel MAC L2 independizada del cortafuegos principal.
*   **Mecanismo de Ejecución:** Los módulos CGI recogen entradas HTTP GET/POST de los usuarios administradores. Para modificar el comportamiento en caliente, los CGIs no ejecutan los archivos `scripts/*` directamente por posibles problemas de permisos de Apache; se comunican enviando strings simples a `127.0.0.1:1234` haciendo uso indirecto de `system/scr_cli`.

---

## 6. Proceso de Instalación (`install/`)

El directorio `install` proporciona las herramientas necesarias para inicializar un sistema base Ubuntu o Debian y convertirlo en el appliance router JSBach.

*   `install`: Script monolítico y modular para preparar el servidor. Realiza las siguientes tareas por fases:
    1.  **Copia de Ficheros (`-f`):** Despliega la estructura del proyecto en `/usr/local/JSBach` y establece permisos restrictivos/root.
    2.  **Instalación de Dependencias (`-a`):** Obtiene paquetes del SO (`net-tools`, `iw`, `apache2`) y habilita/configura virtual hosts para soportar ejecución CGI Bash en Apache.
    3.  **Preparación de Red (`-x`):** Deshabilita y detiene componentes externos (NetworkManager) que puedan interferir en la gestión bruta de interfaces lógicas, y purga IPv6 en nivel kernel y DHCPcd para simplificar el flujo.
    4.  **Servicios (`-s`):** Conecta el router a `systemd` instalando la unidad de arranque y habilitándola de forma persistente.
*   `jsbach_srv.service`: Descriptor de la unidad systemd que arranca `jsbach_srv` en cada inicio del sistema con privilegios de administrador.

---

## 7. Escenarios y Casos de Uso (Use Cases)

A continuación se plantean múltiples escenarios que representan interacciones comunes del usuario/administrador con el ecosistema de JSBach:

### Caso de Uso 1: Instalación desde Cero (Bare-metal)
*   **Actor:** Administrador / Ingeniero de Sistemas.
*   **Descripción:** Preparar un PC basado en Debian/Ubuntu para que actúe como router.
*   **Flujo Normal:**
    1. Obtenido el código fuente del repositorio, el usuario ejecuta el script como superusuario: `sudo bash install/install`.
    2. El script detecta la ausencia de argumentos e invoca el flujo general (-f, -a, -x, -s).
    3. Copia binarios y configuración a `/usr/local/JSBach`.
    4. Descarga `apache2`, detiene e interrumpe de forma permanente a `NetworkManager` e invalida todo el stack IPv6 por kernel (modificando `sysctl`).
    5. Habilita y arranca el demonio `jsbach_srv.service`.
*   **Resultado:** El equipo limpia sus variables de red estandarizadas genéricas para que, en cada rearranque, suba el ecosistema de JSBach con la web accesible localmente, listo para el primer logueo web.

### Caso de Uso 2: Acción Invocada vía Web UI (Desconectar VLAN)
*   **Actor:** Administrador web / Arquitectura de Backend.
*   **Descripción:** A través del dashboard central CGI (`index-admin.cgi`), el administrador identifica problemas en la Zona DMZ e interactúa visualmente con la web para revocar permisos.
*   **Flujo Normal:**
    1. En el navegador, el usuario presiona sobre el botón "Desconnectar" que enlaza a `tallafocs-configuracio.cgi?comand=configurar+desconnectar_input+IN_DMZ`.
    2. El script CGI, ejecutado restringidamente por Apache, procesa la estructura, pero al no tener acceso `root` a iptables, delega la tarea enviando textualmente `tallafocs configurar desconnectar_input IN_DMZ` usando `client_srv_cli` por puerto 1234 TCP.
    3. El demonio residente global en root, `scr_cli`, que vive en un pipe `while read` escuchando a Netcat, captura la orden e invoca nativamente al modulo real (`scripts/tallafocs`).
*   **Resultado:** La interfaz devuelve un 200 OK y el demonio interno del equipo en Linux aplicó la regla en tiempo real y sin saltos peligrosos de permisos en el frontend.

### Caso de Uso 3: Despliegue Inicial con Conexión a Internet
*   **Actor:** Administrador de red.
*   **Descripción:** Configurar un entorno en un router físico limpio que tenga un enlace al ISP.
*   **Flujo Normal:**
    1. El usuario modifica la interfaz de salida y el modo de conexión (`dhcp` o `manual`) usando `ifwan configurar ...`.
    2. Invoca `ifwan iniciar`. El módulo obtiene una ip y DNS.
    3. Invoca `enrutar iniciar`. El router se prepara para enrutar el tráfico privado.
*   **Resultado:** El router JSBach tiene acceso al exterior (`ping google.com` con éxito). Todo el router es capaz de aplicar NAT a los futuros clientes.

### Caso de Uso 2: Despliegue de Switch Local y Administración (VLAN 1)
*   **Actor:** Administrador de red.
*   **Descripción:** Conectar un PC en el puerto físico `enp1s0f0` y obtener capacidades de administración.
*   **Flujo Normal:**
    1. A través de la configuración preexistente en `bridge.conf` y `bridge_if.conf`, el demonio principal llama a `bridge iniciar`.
    2. Se crea la interfaz física `br0.1` (Admin) con una IP de puerta de enlace (ej. `10.0.1.1`).
    3. A la interfaz física `enp1s0f0` se le asocia la VLAN 1 usando `PVID untagged`, dejándolo listo como puerto de acceso nativo para administración.
    4. El usuario conecta el PC y mediante configuración estática (o un script externo de DHCP server) accede a la interfaz `br0.1`.
*   **Resultado:** El administrador ahora posee comunicación local con el dispositivo para administrarlo por entorno web/SSH y accede a otras configuraciones.

### Caso de Uso 3: Aislar Zonas y Establecer Restricciones (Cortafuegos)
*   **Actor:** Sistema Automatizado JSBach.
*   **Descripción:** Definir políticas de seguridad entre la red principal (VLAN_Admin) y las redes secundarias (VLAN_Users).
*   **Flujo Normal:**
    1. Se dispara `tallafocs iniciar`. 
    2. En el entorno global, el script dirige el tráfico desde IP origen `10.0.1.0/24` a `IN_ADMIN`. El flujo define que todo desde Admin está permitido (`ACCEPT`).
    3. Sin embargo, para una VLAN subyacente de usuarios (VLAN 3 o 4), se clasifica como `IN_USERS` el cual implementa limitaciones, aceptando explícitamente solo tráfico hacia Internet o limitándolo estrictamente (DNS puerto 53, DCHP puerto 67/68, y pings).
*   **Resultado:** Los usuarios pueden utilizar Internet y resolución DNS, pero están estrictamente bloqueados de atacar a la red DMZ o de administración.

### Caso de Uso 4: Publicar un Servidor Web (DMZ Port-Forwarding)
*   **Actor:** Administrador / Cliente Web Externo.
*   **Descripción:** Existe un servidor web Nginx conectado sobre la `VLAN 2` con una dirección local. Se necesita que sea accesible desde Internet.
*   **Flujo Normal:**
    1. Usando los wrappers o scripts de JSBach, el usuario llama al comando análogo a `dmz configurar afegir 80 tcp 10.0.2.100`.
    2. El script de DMZ escribe esta regla en `dmz.conf`.
    3. Al detectar que el sistema general está activado, en caso afirmativo invoca un reinicio (`aturar` / `iniciar` parcial de DMZ).
    4. Se implanta una regla `PREROUTING DNAT` vinculando la Interfaz WAN (Ej. `enp6s0`), el protocolo `TCP`, el puerto `80` hacia la IP destino `10.0.2.100:80`.
*   **Resultado:** El tráfico externo al puerto 80 es desviado automáticamente al equipo aislado en la DMZ sin comprometer la LAN principal del router.

### Caso de Uso 5: Aplicar Bloqueos Temporales (Control de Eventos o Amenazas)
*   **Actor:** Administrador de seguridad (GUI/CLI).
*   **Descripción:** Frente a un comportamiento sospechoso o corte programado, se necesita cancelar el comportamiento o enrutamiento de una VLAN y el servidor DMZ.
*   **Flujo Normal:**
    1. Vía la interfaz, se invoca a `tallafocs configurar desconnectar_input IN_DMZ`.
    2. El sistema inserta dinámicamente una alerta (`DROP`) como política primaria limitante en la cadena `IN_DMZ`.
    3. Alternativamente, utilizando ebtables (`tallafocs ebtables_toggle iface`), el sistema elimina el reenvío de paquetes L2 (Aislamiento de la capa de enlace), bloqueando tráfico entre la boca que conecta esa rama DMZ y el resto del switch.
*   **Resultado:** Aislamiento inmediato a nivel perimetral de un sector de la red o intercara física, que se solventa inmediatamente retirando el comando reverso (ej. `connectar_input`).
