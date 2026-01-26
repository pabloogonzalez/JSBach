#!/bin/bash

# Load configuration
source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Configuració DMZ</title>
    <link rel="stylesheet" href="/style.css">
    <style>
        .rule-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px;
            border-bottom: 1px solid #eee;
        }
        .rule-item:last-child {
            border-bottom: none;
        }
        .rule-info {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }
        .rule-port {
            font-weight: 600;
            color: #1a73e8;
            width: 80px;
        }
        .rule-proto {
            text-transform: uppercase;
            font-weight: 500;
            width: 60px;
        }
        .rule-ip {
            font-family: monospace;
            color: #666;
        }
    </style>
</head>
<body>

<nav class="navbar">
    <a href="/cgi-bin/main.cgi" class="navbar-brand">
        <span>📶</span> Router Admin
    </a>
    <div class="nav-links">
        <a href="/cgi-bin/ifwan.cgi" class="nav-link">WAN</a>
        <a href="/cgi-bin/enrutar.cgi" class="nav-link">Enrutament</a>
        <a href="/cgi-bin/bridge.cgi" class="nav-link">Bridge</a>
        <a href="/cgi-bin/tallafocs.cgi" class="nav-link">Tallafocs</a>
        <a href="/cgi-bin/dmz.cgi" class="nav-link active">DMZ</a>
    </div>
</nav>

<div class="container">
    <div class="card">
        <div class="card-header">
            <h2 class="card-title">Configuració de Regles DMZ</h2>
        </div>
        <div class="card-body">
            
            <div class="card" style="box-shadow: none; border: 1px solid #eee; margin-bottom: 24px;">
                <div class="card-header" style="background: #f5f5f5; padding: 12px 16px;">
                    <h3 style="margin: 0; font-size: 16px;">Regles de Reenviament Actuals</h3>
                </div>
                <div>
EOF

IFS=$'\n'
for iface in $($DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli dmz configurar mostrar); do
    PORT=$(echo "$iface"|cut -d';' -f1)
    PROTO=$(echo "$iface"|cut -d';' -f2)
    IP_DMZ=$(echo "$iface"|cut -d';' -f3)
    
    echo "<div class='rule-item'>"
    echo "  <div class='rule-info'>"
    echo "    <span class='rule-port'>Port $PORT</span>"
    echo "    <span class='rule-proto'>$PROTO</span>"
    echo "    <span class='rule-ip'>Cap a $IP_DMZ</span>"
    echo "  </div>"
    echo "  <a href='/cgi-bin/dmz-eliminar.cgi?port=$PORT&proto=$PROTO&ipdmz=$IP_DMZ' class='btn secondary' style='color: #d93025; border-color: #d93025; padding: 4px 12px; font-size: 13px;'>Eliminar</a>"
    echo "</div>"
done

cat << EOF
                </div>
            </div>

            <div style="display: flex; gap: 12px; justify-content: flex-end; margin-top: 24px;">
                <a href="/cgi-bin/dmz-nou-servei.cgi" class="btn">Obrir Nou Servei</a>
                <a href="/cgi-bin/dmz.cgi" class="btn secondary">Tornar a DMZ</a>
            </div>
        </div>
    </div>
</div>

</body>
</html>
EOF



