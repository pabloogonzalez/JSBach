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
# For bridge/firewall, we just check output content crudely for now or improve script output later
# Assuming client_srv_cli returns standard output we saw earlier

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
                <p><strong>Estat:</strong> $STATUS_WAN</p>
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
                <div style="margin-top:8px;">$STATUS_ROUTE</div>
            </div>
        </a>

        <!-- Bridge Card -->
        <a href="/cgi-bin/bridge.cgi" class="card">
            <div class="card-header">
                <span class="card-title">🌉 Bridge</span>
                <span class="card-status status-active">Gestió</span>
            </div>
            <div class="card-body">
                <p>Configuració de VLANs i interfícies pont.</p>
            </div>
        </a>

        <!-- Firewall Card -->
        <a href="/cgi-bin/tallafocs.cgi" class="card">
            <div class="card-header">
                <span class="card-title">🛡️ Tallafocs</span>
                <span class="card-status status-active">Seguretat</span>
            </div>
            <div class="card-body">
                <p>Regles de filtratge i seguretat de la xarxa.</p>
            </div>
        </a>
    </div>
</div>

</body>
</html>
EOF
