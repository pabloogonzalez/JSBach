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
    <title>Configuració Tallafocs</title>
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
        <a href="/cgi-bin/tallafocs.cgi" class="nav-link active">Tallafocs</a>
    </div>
</nav>

<div class="container">
    <div class="card">
        <div class="card-header">
            <h2 class="card-title">Gestió de Connexions i VLANs</h2>
        </div>
        <div class="card-body">

<div class="dashboard-grid" style="grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));">
EOF

for linia in $(grep -v '#' "$DIR/$PROJECTE/$DIR_CONF/$BRIDGE_CONF"); do
    nom=$(echo "$linia"|cut -d';' -f1)
    id=$(echo "$linia"|cut -d';' -f2)
    ip=$(echo "$linia"|cut -d';' -f3)
    estat_vlan=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs estat $id)
    
    # Status styling
    STATUS_CLASS="status-inactive"
    STATUS_ICON="✗"
    if [ "$estat_vlan" == "CONNECTADA" ]; then
        STATUS_CLASS="status-active"
        STATUS_ICON="✓"
    fi

    echo "<div class='card' style='box-shadow: none; border: 1px solid #eee; background: #f9f9f9;'>"
    echo "  <div class='card-header' style='margin-bottom: 10px;'>"
    echo "    <span style='font-weight: 600; font-size: 16px;'>$nom</span>"
    echo "    <span class='card-status $STATUS_CLASS'>$STATUS_ICON $estat_vlan</span>"
    echo "  </div>"
    echo "  <div style='margin-bottom: 15px; color: #666; font-size: 13px;'>"
    echo "    <strong>ID:</strong> $id &nbsp;|&nbsp; <strong>Subnet:</strong> $ip"
    echo "  </div>"
    
    echo "  <div style='display: flex; gap: 8px; flex-wrap: wrap;'>"
    if [ "$estat_vlan" == "CONNECTADA" ]; then
        echo "    <a href='tallafocs-conndeconn.cgi?id=$id&accio=desconnectar' class='btn secondary' style='color: var(--danger-color); border-color: var(--danger-color); flex: 1; text-align: center;'>DESCONNECTAR</a>"
    else
        echo "    <a href='tallafocs-conndeconn.cgi?id=$id&accio=connectar' class='btn' style='flex: 1; text-align: center;'>CONNECTAR</a>"
        echo "    <a href='tallafocs-conndeconn.cgi?id=$id&accio=connectar_port_wls' class='btn secondary' style='flex: 1; text-align: center;'>LIMITAR PORTS</a>"
    fi
    echo "  </div>"
    echo "</div>"
done

cat << EOF
</div>

<div style="margin-top: 24px; text-align: right;">
    <a href="/cgi-bin/tallafocs.cgi" class="btn secondary">Tornar al Tallafocs</a>
</div>

        </div>
    </div>
</div>
</body>
</html>
EOF
