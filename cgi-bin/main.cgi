#!/bin/bash

# Load variables
source /usr/local/JSBach/conf/variables.conf
source $DIR/$PROJECTE/$DIR_CONF/$CONF_IFWAN

# Helper function to get status text/color
get_status_html() {
    local status="$1"
    if [[ "$status" == *"ACTIVAT"* ]] || [[ "$status" == "UP" ]]; then
        echo "<span class='card-status status-active'>ACTIU</span>"
    else
        echo "<span class='card-status status-inactive'>INACTIU</span>"
    fi
}

# Fetch statuses
STATUS_WAN=$($DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli ifwan estat)
STATUS_ROUTE=$($DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli enrutar estat)
STATUS_BRIDGE_RESUM=$($DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli bridge resum)
STATUS_FIREWALL_RESUM=$($DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli tallafocs resum)
STATUS_WIFI=$($DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli wifi estat)
STATUS_DHCP=$($DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli dhcp estat | head -n 1)

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JSBach Router Admin</title>
    <link rel="stylesheet" href="/style.css">
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
        <a href="/cgi-bin/wifi.cgi" class="nav-link">WiFi</a>
        <a href="/cgi-bin/dmz.cgi" class="nav-link">DMZ</a>
        <a href="/cgi-bin/ebtables.cgi" class="nav-link">Ebtables</a>
        <a href="/cgi-bin/switchs.cgi" class="nav-link">Switchs</a>
    </div>
</nav>

<div class="container">
    <h2>Panell de Control</h2>
    
    <div class="dashboard-grid">
        <!-- WAN Card -->
        <a href="/cgi-bin/ifwan.cgi" class="card">
            <div class="card-header">
                <span class="card-title">🌐 WAN</span>
                $(get_status_html "$STATUS_WAN")
            </div>
            <div class="card-body">
                <p>Configuració de xarxa externa i estat de connexió.</p>
                <p style="margin-top:8px;"><strong>Estat:</strong> $STATUS_WAN</p>
            </div>
        </a>

        <!-- WiFi Card -->
        <a href="/cgi-bin/wifi.cgi" class="card">
            <div class="card-header">
                <span class="card-title">📶 WiFi</span>
                $(get_status_html "$STATUS_WIFI")
            </div>
            <div class="card-body">
                <p>Configuració del Punt d'Accés WiFi i seguretat.</p>
                <div style="margin-top:8px;"><strong>Estat:</strong> $STATUS_WIFI</div>
            </div>
        </a>

        <!-- Routing Card -->
        <a href="/cgi-bin/enrutar.cgi" class="card">
            <div class="card-header">
                <span class="card-title">🔀 Enrutament</span>
                $(get_status_html "$STATUS_ROUTE")
            </div>
            <div class="card-body">
                <p>Gestió de NAT i reenviament de paquets.</p>
                <div style="margin-top:8px;"><strong>Estat:</strong> $STATUS_ROUTE</div>
            </div>
        </a>

        <!-- Bridge Card -->
        <a href="/cgi-bin/bridge.cgi" class="card">
            <div class="card-header">
                <span class="card-title">🌉 Bridge</span>
                $(get_status_html "$STATUS_BRIDGE_RESUM")
            </div>
            <div class="card-body">
                <p>Configuració de VLANs i interfícies pont.</p>
                <div style="margin-top:8px;"><strong>Estat:</strong> $STATUS_BRIDGE_RESUM</div>
            </div>
        </a>

        <!-- Firewall Card -->
        <a href="/cgi-bin/tallafocs.cgi" class="card">
            <div class="card-header">
                <span class="card-title">🛡️ Tallafocs</span>
                $(get_status_html "$STATUS_FIREWALL_RESUM")
            </div>
            <div class="card-body">
                <p>Regles de filtratge i seguretat de la xarxa.</p>
                <div style="margin-top:8px;"><strong>Estat:</strong> $STATUS_FIREWALL_RESUM</div>
            </div>
        </a>

        <!-- DMZ Card -->
        <a href="/cgi-bin/dmz.cgi" class="card">
            <div class="card-header">
                <span class="card-title">📦 DMZ</span>
                $(source /usr/local/JSBach/conf/variables.conf && get_status_html "$($DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli dmz estat | head -n 1)")
            </div>
            <div class="card-body">
                <p>Configuració de desmilitarització i obertura de ports cap a hosts interns.</p>
                <div style="margin-top:8px;"><strong>Estat:</strong> $($DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli dmz estat | head -n 1)</div>
            </div>
        </a>

        <!-- DHCP Card -->
        <a href="/cgi-bin/dhcp.cgi" class="card">
            <div class="card-header">
                <span class="card-title">🔌 DHCP</span>
                $(get_status_html "$STATUS_DHCP")
            </div>
            <div class="card-body">
                <p>Assignació automàtica d'IPs a usuaris i dispositius de xarxa via dnsmasq.</p>
                <div style="margin-top:8px;"><strong>Estat:</strong> $STATUS_DHCP</div>
            </div>
        </a>

        <!-- Ebtables Card -->
        <a href="/cgi-bin/ebtables.cgi" class="card">
            <div class="card-header">
                <span class="card-title">🧱 Ebtables</span>
                <span class="card-status status-active">L2</span>
            </div>
            <div class="card-body">
                <p>Aïllament d'interfícies físiques (Layer 2) i regles de pont.</p>
                <div style="margin-top:8px;">Gestió de regles Ebtables</div>
            </div>
        </a>
        
        <!-- Switchs Card -->
        <a href="/cgi-bin/switchs.cgi" class="card">
            <div class="card-header">
                <span class="card-title">🖧 Switchs</span>
                $(source /usr/local/JSBach/conf/variables.conf && get_status_html "$($DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli switchs estat | grep 'FUNCIONA' | wc -l) Actius")
            </div>
            <div class="card-body">
                <p>Gestió d'infraestructura de xarxa (Switchs).</p>
                <div style="margin-top:8px;"><strong>Total:</strong> $($DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli switchs estat | wc -l) Dispositiu(s)</div>
            </div>
        </a>

        <!-- Port Mirroring Card -->
        <a href="/cgi-bin/portmirror.cgi" class="card">
            <div class="card-header">
                <span class="card-title">🔍 Port Mirroring</span>
                $(source /usr/local/JSBach/conf/variables.conf && get_status_html "$($DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror estat | head -n 1)")
            </div>
            <div class="card-body">
                <p>Còpia i anàlisi de trànsit de xarxa per inspecció.</p>
                <div style="margin-top:8px;"><strong>Estat:</strong> $($DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror estat | head -n 1)</div>
            </div>
        </a>
    </div>
</div>

</body>
</html>
EOF
