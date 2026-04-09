#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Configuració Port Mirroring</title>
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
        <a href="/cgi-bin/portmirror.cgi" class="nav-link active">Port Mirroring</a>
    </div>
</nav>

<div class="container">
    <div class="card">
        <div class="card-header">
            <h2 class="card-title">Configurar Port Mirroring</h2>
        </div>
        <div class="card-body">
            <div style="margin-bottom: 20px;">
                <a href="/cgi-bin/portmirror.cgi" class="btn secondary">← Tornar a Port Mirror</a>
            </div>
EOF

ESTAT_PORTMIRROR=$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror estat)
if [[ "$ESTAT_PORTMIRROR" == $ACTIVAT* ]]; then
    echo "<div class='alert' style='background-color: var(--danger-color); color: white; padding: 15px; border-radius: 8px;'>"
    echo "<h3>⚠️ Error: Port Mirroring Activado</h3>"
    echo "<p>Para poder configurar, Port Mirroring <strong>debe estar desactivado</strong>.</p>"
    echo "</div><br>"
    INTERFACE_SENSOR=$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror mostrar interface_sensor)
    echo "<p><strong>Interfaç sensor (Captures):</strong> $INTERFACE_SENSOR</p>"
    echo "<br>"
    LLISTA_INTEFACES=$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror mostrar interfaces_aptes_sensor)
    echo "<p><strong>Interfícies monitoritzades:</strong> $LLISTA_INTEFACES</p>"
    echo "<br>"
    echo "<pre>$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror estat)</pre>"
else
    echo "<h3>1. Interfaç Sensor (on s'envien les captures)</h3>"
    INTERFACE_SENSOR=$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror mostrar interface_sensor)
    if [ -z "$INTERFACE_SENSOR" ]; then
        echo "<p style='color: var(--danger-color);'><strong>Estat:</strong> NO SELECCIONADA</p>"
    else
        echo "<p style='color: var(--primary-color);'><strong>Estat Actual:</strong> $INTERFACE_SENSOR</p>"
    fi
    
    echo "<p><em>* No pot formar part del bridge ni estar activada</em></p>"
    LLISTA_INTEFACES=$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror mostrar interfaces_aptes_sensor)
    echo "<form method=\"get\" action=\"/cgi-bin/portmirror.cgi\" class='form-group' style='max-width: 400px; display: flex; gap: 10px; align-items: center;'>"
    echo "<input type='hidden' name='comand' value='configurar'>"
    echo "<input type='hidden' name='argument' value='canviar_interface_sensor'>"
    echo "<input type='hidden' name='retorn' value='portmirror-configurar.cgi'>"
    echo "<select name=\"interface_sensor\" class='form-control'>"
    for interface in $LLISTA_INTEFACES
    do
        if [ "$interface" == "$INTERFACE_SENSOR" ]; then
            echo "<option value=\"$interface\" selected>$interface</option>"
        else
            echo "<option value=\"$interface\">$interface</option>"
        fi
    done
    echo "</select>"
    echo "<input type=\"submit\" value=\"Canviar Sensor\" class='btn btn-primary'>"
    echo "</form>"
    echo "<hr class='my-4'>"

    echo "<h3>2. Interfícies origen (d'on es fan les captures)</h3>"
    INTERFACES_LAN=$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror mostrar interfaces_lan)

    echo "<form action='/cgi-bin/portmirror.cgi' method='get'>"
    echo "<input type='hidden' name='comand' value='configurar'>"
    echo "<input type='hidden' name='argument' value='modificar_interfaces_lan'>"
    echo "<input type='hidden' name='retorn' value='portmirror-configurar.cgi'>"
    echo "<table class='table' style='max-width: 400px;'>"
    echo "<thead><tr><th>Interfaç</th><th>Capturar</th></tr></thead>"
    echo "<tbody>"
    LLISTA_INTEFACES=$(ip -o link show | awk -F': ' '{print $2}')
    mapfile -t LLISTA_INTEFACES <<< "$LLISTA_INTEFACES"

    for ((i = 0; i < ${#LLISTA_INTEFACES[@]}; i++)); do
        interface="${LLISTA_INTEFACES[$i]}"
        [ -z "$interface" ] && continue
        [ "$interface" == "$INTERFACE_SENSOR" ] && continue
        echo "<tr><td><strong>$interface</strong></td>"
        if [[ $(echo "$INTERFACES_LAN" | grep "$interface")   ]]; then
            echo "<td><input type='checkbox' name='$interface' value='$interface' checked></td></tr>"
        else
            echo "<td><input type='checkbox' name='$interface' value='$interface'></td></tr>"
        fi
    done
    echo "</tbody></table>"
    echo "<input type='submit' value='Guardar Interfícies' class='btn btn-primary mt-3'>"
    echo "</form>"
fi

cat << EOF
        </div>
    </div>
</div>
</body>
</html>
EOF
