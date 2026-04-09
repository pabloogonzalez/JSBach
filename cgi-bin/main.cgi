#!/bin/bash

# Es buena práctica asegurar que se imprimen las cabeceras CGI correctas:
echo -e "Content-type: text/html\n"

source /usr/local/JSBach/conf/variables.conf

# Volcado del código HTML generado dinámicamente con bash
/bin/cat << EOM
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Administración de JSBach - $HOSTNAME</title>
    
    <!-- Configuración para evitar el caché durante el desarrollo web -->
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    
    <!-- Icons (FontAwesome CDN) -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Tailwind CSS (Usando CDN, ideal para integrarlo rápido sin compilar node_modules acá) -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        brand: {
                            bg: '#0f172a',      // Slate 950 (Fondo principal main)
                            card: '#1e293b',    // Slate 800 (Fondo tarjetas y sidebar)
                            border: '#334155',  // Slate 700 (Bordes y separadores)
                            cyan: '#06b6d4',
                            emerald: '#10b981',
                            magenta: '#d946ef',
                        }
                    },
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                        mono: ['JetBrains Mono', 'monospace'], // Usada para IPs y Tráfico
                    }
                }
            }
        }
    </script>

    <!-- Chart.js para gráficos -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <!-- Estilos locales inline (Scrollbars para no romper el aspecto hacker/industrial) -->
    <style>
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: #0f172a; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #475569; }
    </style>
</head>
<body class="bg-brand-bg text-slate-300 font-sans h-screen flex overflow-hidden antialiased">

    <!-- ============================================
         SIDEBAR (Sustituye al antiguo model.cgi)
         ============================================ -->
    <aside class="w-64 bg-brand-card border-r border-brand-border flex flex-col flex-shrink-0">
        <!-- Brand / Capa Superior -->
        <div class="h-16 flex items-center px-6 border-b border-brand-border">
            <i class="fa-solid fa-shield-halved text-brand-cyan text-2xl mr-3"></i>
            <h1 class="text-xl font-bold tracking-wider text-white">JSBach</h1>
        </div>
        
        <!-- Navegación. IMPORTANTE: Con el atributo target="body" los enlaces se abrirán en el iframe central -->
        <nav class="flex-1 py-4 overflow-y-auto">
            <ul class="space-y-1">
                <li>
                    <a href="/cgi-bin/estat.cgi" target="body" class="flex items-center px-6 py-3 bg-brand-border/30 text-brand-cyan border-r-2 border-brand-cyan transition-colors">
                        <i class="fa-solid fa-chart-line w-6 text-center"></i>
                        <span class="font-medium ml-2">Dashboard</span>
                    </a>
                </li>
                <li>
                    <a href="/cgi-bin/tallafocs-menu.cgi" target="body" class="flex items-center px-6 py-3 text-slate-400 hover:text-white hover:bg-brand-border/20 transition-colors">
                        <i class="fa-solid fa-fire-burner w-6 text-center"></i>
                        <span class="font-medium ml-2">Firewall</span>
                    </a>
                </li>
                <li>
                    <a href="/cgi-bin/bridge-menu.cgi" target="body" class="flex items-center px-6 py-3 text-slate-400 hover:text-white hover:bg-brand-border/20 transition-colors">
                        <i class="fa-solid fa-network-wired w-6 text-center"></i>
                        <span class="font-medium ml-2">Switch/VLANs</span>
                    </a>
                </li>
                <li>
                    <a href="/cgi-bin/ifwan-menu.cgi" target="body" class="flex items-center px-6 py-3 text-slate-400 hover:text-white hover:bg-brand-border/20 transition-colors">
                        <i class="fa-solid fa-globe w-6 text-center"></i>
                        <span class="font-medium ml-2">Red WAN</span>
                    </a>
                </li>
                <li>
                    <a href="/cgi-bin/dmz-menu.cgi" target="body" class="flex items-center px-6 py-3 text-slate-400 hover:text-white hover:bg-brand-border/20 transition-colors">
                        <i class="fa-solid fa-server w-6 text-center"></i>
                        <span class="font-medium ml-2">Zona DMZ</span>
                    </a>
                </li>
                <li>
                    <a href="/cgi-bin/enrutar-menu.cgi" target="body" class="flex items-center px-6 py-3 text-slate-400 hover:text-white hover:bg-brand-border/20 transition-colors">
                        <i class="fa-solid fa-route w-6 text-center"></i>
                        <span class="font-medium ml-2">Enrutamiento NAT</span>
                    </a>
                </li>
            </ul>
        </nav>

        <div class="p-4 border-t border-brand-border text-xs text-slate-500 font-mono">
            JSBach System<br>
            Host: $HOSTNAME
        </div>
    </aside>

    <!-- ============================================
         CONTENIDO PRINCIPAL
         ============================================ -->
    <main class="flex-1 flex flex-col overflow-hidden relative">
        
        <!-- HEADER (Sustituye parcialmente al antiguo index-admin.cgi) -->
        <header class="h-16 flex items-center justify-between px-8 bg-brand-bg border-b border-brand-border flex-shrink-0 z-10 shadow-sm">
            <h2 class="text-lg font-semibold text-white truncate" id="top-title">Vista General del Sistema</h2>
            <div class="flex items-center space-x-4">
                <span class="flex h-3 w-3 relative">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-emerald opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-3 w-3 bg-brand-emerald"></span>
                </span>
                <span class="text-sm font-mono text-slate-400" id="clock">00:00:00</span>
            </div>
        </header>

        <!-- 
             AREA DINÁMICA (IFRAME)
             Aquí es donde se cargarán los scripts tradicionales como estat.cgi o dmz.cgi 
             sin romper la navegación lateral (Menú Fijo). 
             Nota: Si un script anterior carga otro html completo sin transparencias, tapará al fondo,
             por lo cual asegurate de poner `class="bg-transparent"` o `bg-slate-950` en los bodies hijos.
        -->
        <div class="flex-1 w-full h-full relative p-0 overflow-hidden bg-brand-bg">
            <iframe 
                src="/cgi-bin/estat.cgi" 
                name="body" 
                class="w-full h-full border-none block"
                id="mainIframe">
            </iframe>
        </div>

    </main>

    <!-- SCRIPT DE FRONTEND BASICO -->
    <script>
        // Inicializar reloj
        setInterval(() => {
            const now = new Date();
            document.getElementById('clock').innerText = now.toLocaleTimeString('es-ES');
        }, 1000);

        // Dinamismo super sencillo: Actualizar el título cuando clickeamos en el menu lateral
        document.querySelectorAll('aside nav a').forEach(link => {
            link.addEventListener('click', function(e) {
                // Sacar estilo activo a los demás
                document.querySelectorAll('aside nav a').forEach(el => {
                    el.classList.remove('bg-brand-border/30', 'text-brand-cyan', 'border-r-2', 'border-brand-cyan');
                    el.classList.add('text-slate-400');
                });
                // Estilo activo para el clicado
                this.classList.remove('text-slate-400');
                this.classList.add('bg-brand-border/30', 'text-brand-cyan', 'border-r-2', 'border-brand-cyan');
                
                // Actualizar titulo
                const name = this.querySelector('span').innerText;
                document.getElementById('top-title').innerText = name;
            });
        });
    </script>
</body>
</html>
EOM
