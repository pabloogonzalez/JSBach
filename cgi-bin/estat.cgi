#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo -e "Content-type: text/html; charset=utf-8\n"

/bin/cat << 'EOM'
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>JSBach Dashboard</title>
  
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  
  <!-- Carga de Tailwind CSS (Motor Principal JIT) -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
      tailwind.config = {
          darkMode: 'class',
          theme: {
              extend: {
                  colors: {
                      brand: {
                          bg: '#0f172a',      
                          card: '#1e293b',    
                          border: '#334155',  
                          cyan: '#06b6d4',
                          emerald: '#10b981',
                          magenta: '#d946ef',
                      }
                  }
              }
          }
      }
  </script>

  <!-- Carga de Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

EOM

# Inyectar estilos globales (Para que las etiquetas de backend se transformen a Terminal Estilo Hacker)
cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN

/bin/cat << 'EOM'
</head>
<body class="bg-transparent text-slate-300 font-sans p-6 overflow-x-hidden">

<div class="mb-8 border-b border-brand-border pb-4">
    <h2 class="text-2xl font-bold text-white mb-2 !bg-transparent !border-none !p-0 !shadow-none !mt-0">Métricas Principales</h2>
    <p class="text-slate-400 text-sm">Rendimiento en tiempo real de JSBach</p>
</div>

<!-- ==============================================
     1. TERCIO SUPERIOR: KPI CARDS
     ============================================== -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
    
    <!-- CPU -->
    <div class="bg-brand-card border border-brand-border p-5 rounded-sm flex items-center shadow-lg">
        <div class="relative w-14 h-14 flex items-center justify-center mr-4">
            <svg class="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                <path class="text-brand-border" stroke-width="3" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                <path class="text-brand-cyan" stroke-dasharray="25, 100" stroke-width="3" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" id="cpu-ring" />
            </svg>
            <span class="absolute text-xs font-mono font-bold text-white tracking-tighter" id="cpu-val">25%</span>
        </div>
        <div>
            <h3 class="!bg-transparent !border-none !p-0 !text-xs !mb-1 text-slate-400">Carga de CPU</h3>
            <div class="font-mono text-sm">4 Núcleos @ 1.8GHz</div>
        </div>
    </div>

    <!-- RAM -->
    <div class="bg-brand-card border border-brand-border p-5 rounded-sm flex flex-col justify-center shadow-lg">
        <div class="flex justify-between items-end mb-2">
            <h3 class="!bg-transparent !border-none !p-0 !text-xs text-slate-400">Memoria RAM</h3>
            <span class="font-mono text-sm font-bold text-white" id="ram-val">45%</span>
        </div>
        <div class="w-full bg-brand-bg h-2 rounded-full overflow-hidden border border-brand-border">
            <div class="bg-brand-emerald h-full transition-all duration-500 ease-in-out" style="width: 45%" id="ram-bar"></div>
        </div>
        <div id="ram-desc" class="text-xs font-mono text-slate-500 mt-2 text-right">-- GB / -- GB</div>
    </div>

    <!-- DISK -->
    <div class="bg-brand-card border border-brand-border p-5 rounded-sm flex items-center justify-between shadow-lg">
        <div>
            <h3 class="!bg-transparent !border-none !p-0 !text-xs !mb-1 text-slate-400">Almacenamiento</h3>
            <div class="flex items-baseline space-x-1">
                <span id="disk-val" class="text-3xl font-mono font-bold text-white">--</span>
                <span class="text-sm font-mono text-slate-500">% Utilizado</span>
            </div>
        </div>
        <i class="fa-solid fa-hard-drive text-3xl text-brand-cyan opacity-80"></i>
    </div>

    <!-- UPTIME -->
    <div class="bg-brand-card border border-brand-border p-5 rounded-sm flex items-center justify-between shadow-lg">
        <div>
            <h3 class="!bg-transparent !border-none !p-0 !text-xs !mb-1 text-slate-400">Tiempo Actividad</h3>
            <div class="text-xl font-mono font-bold text-white" id="uptime-val">---</div>
        </div>
        <i class="fa-solid fa-stopwatch text-3xl text-brand-emerald opacity-80"></i>
    </div>
</div>

<!-- ==============================================
     2. PARTE CENTRAL: MONITOR DE RED (CHART)
     ============================================== -->
<div class="bg-brand-card border border-brand-border rounded-sm p-6 mb-12 relative shadow-lg">
    <div class="flex justify-between items-center mb-4">
        <h3 class="!bg-transparent !border-none !p-0 !text-sm text-white font-bold">Tráfico de Red (enp1s0 WAN)</h3>
        <div class="flex space-x-4 text-xs font-mono">
            <div class="flex items-center"><span class="w-3 h-3 bg-brand-cyan rounded-full mr-2"></span>Download: <span id="dl-rate" class="ml-1 text-white">0.0 Mbps</span></div>
            <div class="flex items-center"><span class="w-3 h-3 bg-brand-magenta rounded-full mr-2"></span>Upload: <span id="ul-rate" class="ml-1 text-white">0.0 Mbps</span></div>
        </div>
    </div>
    <div class="w-full h-80">
        <canvas id="networkChart"></canvas>
    </div>
</div>

<!-- ==============================================
     3. MITAD INFERIOR: ESTADO DE LÓGICA (BADGES)
     ============================================== -->
<div class="my-6 border-b border-brand-border pb-4 mt-8">
    <h2 class="text-xl font-bold text-white mb-2 !bg-transparent !border-none !p-0 !shadow-none !mt-0">Estado de Servicios</h2>
    <p class="text-slate-400 text-sm">Monitorización de subsistemas troncales</p>
</div>

<!-- Rejilla Visual -->
<div id="service-badges-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-10">
EOM

# --- FUNCIÓN: RENDERIZAR ESTATUS (DESCRIPTIVO HUMANO CON ENLACES) ---
function print_status_badge {
  local title=$1
  local icon=$2
  local value=$3
  
  local state
  local color_class
  local dot_class
  local description
  local href="#"
  
  # Usamos grep para detectar la bandera exclusiva ACTIVAT filtrando explícitamente posibles DESACTIVAT
  if echo "$value" | grep -i "ACTIVAT" | grep -q -v -i "DESACTIVAT"; then
     state="ONLINE"
     color_class="text-brand-emerald border-brand-emerald/30 bg-brand-emerald/10"
     dot_class="bg-brand-emerald shadow-[0_0_8px_rgba(16,185,129,0.8)]"
  else
     state="OFFLINE"
     color_class="text-slate-500 border-brand-border bg-[#141e30]"
     dot_class="bg-slate-600"
  fi

  # Rutas a CGI relativas
  case "$title" in
    "Red Externa (WAN)") href="/cgi-bin/ifwan-menu.cgi"; description="Interfaz de área amplia vinculada y operativa en el núcleo." ;;
    "Enrutamiento (NAT)") href="/cgi-bin/enrutar-menu.cgi"; description="Reglas de enmascaramiento dinámico (Masquerade) activadas." ;;
    "Switch & VLANs") href="/cgi-bin/bridge-menu.cgi"; description="Puente lógico principal activo y segmentando topología L2." ;;
    "Punto de Acceso WiFi") href="/cgi-bin/wifi-menu.cgi"; description="Módulo Hotspot emitiendo señal inalámbrica y aislando clientes WiFi." ;;
    "Túnel VPN (Op/Wg)") href="/cgi-bin/vpn_wg-menu.cgi"; description="Demonios de cifrado escuchando conexiones entrantes de clientes VPN." ;;
    "Servidor DHCP") href="/cgi-bin/dhcp-menu.cgi"; description="Servicio Dnsmasq despachando IPs de enrutamiento dinámicamente." ;;
    "Firewall Restrictivo") href="/cgi-bin/tallafocs-menu.cgi"; description="Políticas de cortafuegos IPTables aislando y repeliendo el tráfico." ;;
    "Reenvío DMZ / Puertos") href="/cgi-bin/dmz-menu.cgi"; description="Traduciendo peticiones públicas directas hacia los servidores en DMZ." ;;
    "Portal Cautivo") href="/cgi-bin/portal_captiu-menu.cgi"; description="Portal logístico en funcionamiento detectando nuevas MACs." ;;
  esac

  if [[ "$state" == "OFFLINE" ]]; then
     description="Este servicio se encuentra desconectado, apagado o sin reglas aplicadas."
  fi

  # Envolvemos absolutamente todo en una etiqueta <a> super estilizada
  echo "<a href='$href' onclick=\"if(window.top && window.top.document) { Array.from(window.top.document.querySelectorAll('aside nav a')).forEach(el => { el.classList.remove('bg-brand-border/30', 'text-brand-cyan', 'border-r-2'); el.classList.add('text-slate-400'); if(el.href.includes('$href')) { el.classList.remove('text-slate-400'); el.classList.add('bg-brand-border/30', 'text-brand-cyan', 'border-r-2'); window.top.document.getElementById('top-title').innerText = el.querySelector('span').innerText; } }); }\" class='block bg-brand-card border border-brand-border rounded-lg p-5 flex flex-col shadow-sm hover:border-brand-emerald/40 hover:bg-[#1a2536] hover:shadow-md hover:-translate-y-[2px] transition-all duration-200 cursor-pointer'>"
  echo "  <div class='flex items-center justify-between mb-3'>"
  echo "    <div class='flex items-center space-x-4'>"
  echo "      <div class='w-10 h-10 rounded-full bg-[#141e30] flex items-center justify-center text-slate-400 border border-brand-border transition-colors group-hover:text-brand-cyan'><i class='$icon w-4 text-center'></i></div>"
  echo "      <div><h4 class='text-sm font-bold text-slate-200 m-0'>$title</h4></div>"
  echo "    </div>"
  echo "    <div class='flex items-center px-3 py-1 rounded-full border $color_class text-[11px] font-mono font-bold uppercase tracking-wider'>"
  echo "      <span class='w-2 h-2 rounded-full $dot_class mr-2'></span> $state"
  echo "    </div>"
  echo "  </div>"

  echo "  <div class='mt-1 text-[13px] text-slate-400 leading-relaxed font-sans'>"
  echo "    $description"
  echo "  </div>"
  echo "</a>"
}

# --- EJECUCIÓN (Asíncrona al backend) ---
RES_IFWAN=$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli ifwan estat)
RES_ENRUTAR=$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli enrutar estat)
RES_BRIDGE=$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge estat)
RES_WIFI=$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli wifi estat)
RES_VPN=$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli vpn_wg estat)
RES_DHCP=$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dhcp estat)
RES_TALLAFOCS=$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs estat)
RES_DMZ=$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dmz estat)
RES_PORTAL=$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portal_captiu estat)

# --- IMPRESIÓN (Badges en vez de HTML/CLI Bruto) ---
print_status_badge "Red Externa (WAN)" "fa-solid fa-globe" "$RES_IFWAN"
print_status_badge "Enrutamiento (NAT)" "fa-solid fa-route" "$RES_ENRUTAR"
print_status_badge "Switch & VLANs" "fa-solid fa-network-wired" "$RES_BRIDGE"
print_status_badge "Punto de Acceso WiFi" "fa-solid fa-wifi" "$RES_WIFI"
print_status_badge "Túnel VPN (Op/Wg)" "fa-solid fa-lock" "$RES_VPN"
print_status_badge "Servidor DHCP" "fa-solid fa-server" "$RES_DHCP"
print_status_badge "Firewall Restrictivo" "fa-solid fa-fire-burner" "$RES_TALLAFOCS"
print_status_badge "Reenvío DMZ / Puertos" "fa-solid fa-door-open" "$RES_DMZ"
print_status_badge "Portal Cautivo" "fa-solid fa-shield" "$RES_PORTAL"

/bin/cat << 'EOM'
</div>

<!-- ==============================================
     SCRIPTS AJAS PARA TELEMETRÍA EN TIEMPO REAL
     ============================================== -->
<script>
    // Configuración Inicial de CHART.JS
    const ctx = document.getElementById('networkChart').getContext('2d');
    
    // Gradientes visuales
    const gradientDL = ctx.createLinearGradient(0, 0, 0, 300);
    gradientDL.addColorStop(0, 'rgba(6, 182, 212, 0.4)');
    gradientDL.addColorStop(1, 'rgba(6, 182, 212, 0)');

    const gradientUL = ctx.createLinearGradient(0, 0, 0, 300);
    gradientUL.addColorStop(0, 'rgba(217, 70, 239, 0.4)');
    gradientUL.addColorStop(1, 'rgba(217, 70, 239, 0)');

    const dataLength = 25;
    let labels = Array.from({length: dataLength}, () => '');
    let dlData = Array.from({length: dataLength}, () => 0);
    let ulData = Array.from({length: dataLength}, () => 0);

    const networkChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                { label: 'Download', borderColor: '#06b6d4', backgroundColor: gradientDL, borderWidth: 2, fill: true, tension: 0.4, pointRadius: 0, hoverRadius: 4, data: dlData },
                { label: 'Upload', borderColor: '#d946ef', backgroundColor: gradientUL, borderWidth: 2, fill: true, tension: 0.4, pointRadius: 0, hoverRadius: 4, data: ulData }
            ]
        },
        options: {
            responsive: true, 
            maintainAspectRatio: false,
            animation: { duration: 600, easing: 'linear' },
            plugins: { 
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    titleColor: '#94a3b8',
                    bodyColor: '#e2e8f0',
                    borderColor: '#334155',
                    borderWidth: 1,
                    font: { family: 'JetBrains Mono' }
                }
            },
            scales: {
                x: { grid: { display: false, drawBorder: false }, ticks: { display: false } },
                y: { 
                    grid: { color: '#334155', tickLength: 0 }, border: { display: false }, min: 0, suggestedMax: 100, 
                    ticks: { color: '#94a3b8', font: { family: 'JetBrains Mono', size: 11 }, callback: v => v + ' M' } 
                }
            }
        }
    });

    // -------------------------------------------------------------
    // MOTOR DE ACTUALIZACIÓN (AJAX)
    // -------------------------------------------------------------
    let lastRx = -1;
    let lastTx = -1;
    let lastTime = Date.now();
    let tickCounter = 0;

    function updateDashboard() {
        tickCounter++;

        // 1. OBTENER MÉTRICAS REALES DE LA MÁQUINA CADA 2 SEGS
        fetch('/cgi-bin/metricas_api.cgi')
            .then(r => r.json())
            .then(data => {
                // Actualizar Textos
                document.getElementById('uptime-val').innerText = data.uptime;
                document.getElementById('cpu-val').innerText = data.cpu + '%';
                document.getElementById('ram-val').innerText = data.ram_percent + '%';
                document.getElementById('ram-desc').innerText = data.ram_text;
                document.getElementById('disk-val').innerText = data.disk;

                // Animaciones Circulares y de Barras
                document.getElementById('cpu-ring').setAttribute('stroke-dasharray', `${data.cpu}, 100`);
                document.getElementById('ram-bar').style.width = data.ram_percent + '%';

                // Cálculo Deltas de Red (Mbps)
                if (lastRx !== -1) {
                    const now = Date.now();
                    const secondsDiff = (now - lastTime) / 1000;
                    
                    // Velocidad = Bits / Tiempo / Megabit
                    let dlRate = ((data.rx_bytes - lastRx) * 8) / 1000000 / secondsDiff;
                    let ulRate = ((data.tx_bytes - lastTx) * 8) / 1000000 / secondsDiff;

                    if(dlRate < 0) dlRate = 0;
                    if(ulRate < 0) ulRate = 0;

                    document.getElementById('dl-rate').innerText = dlRate.toFixed(1) + ' Mbps';
                    document.getElementById('ul-rate').innerText = ulRate.toFixed(1) + ' Mbps';

                    // Modificar array Chart y refrescar
                    dlData.push(dlRate); dlData.shift();
                    ulData.push(ulRate); ulData.shift();
                    
                    // Escalar enp1s0 dynamically
                    const p1s0Label = document.querySelector('h3.text-white.font-bold');
                    if(p1s0Label && data.interface && data.interface != "") {
                       p1s0Label.innerText = 'Tráfico de Red (' + data.interface + ')';
                    }

                    networkChart.update();
                }

                lastRx = data.rx_bytes;
                lastTx = data.tx_bytes;
                lastTime = Date.now();
            })
            .catch(console.error);

        // 2. REFRESCO BACKGROUND DEL ESTADO (CADA ~30 SEGUNDOS)
        // Soluciona el bug de apagado remoto sin tener que reiniciar la página ni romper el gráfico.
        if (tickCounter > 15) {
            tickCounter = 0;
            fetch('/cgi-bin/estat.cgi')
                .then(r => r.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const domNuevoGrid = doc.getElementById('service-badges-grid');
                    if (domNuevoGrid) {
                        document.getElementById('service-badges-grid').innerHTML = domNuevoGrid.innerHTML;
                    }
                })
                .catch(console.error);
        }
    }

    // Inicializar el puente
    setInterval(updateDashboard, 2000);
</script>

</body>
</html>
EOM
