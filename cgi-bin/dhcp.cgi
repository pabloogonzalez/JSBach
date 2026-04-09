#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

comand=$(echo "$QUERY_STRING" | sed -n 's/^.*comand=\([^&]*\).*$/\1/p')

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Servei DHCP</title>
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
        <a href="/cgi-bin/dhcp.cgi" class="nav-link active">DHCP</a>
    </div>
</nav>

<div class="container">
    <div class="card">
        <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
            <h2 class="card-title">Estat del Servei DHCP</h2>
            <div>
                <a href="/cgi-bin/dhcp.cgi?comand=iniciar" class="btn btn-primary">Iniciar</a>
                <a href="/cgi-bin/dhcp.cgi?comand=aturar" class="btn btn-danger">Aturar</a>
                <a href="/cgi-bin/dhcp.cgi?comand=estat" class="btn secondary">Estat Complet</a>
                <a href="/cgi-bin/dhcp-configurar.cgi" class="btn secondary">Configuració</a>
            </div>
        </div>
        <div class="card-body">
EOF

case "$comand" in
    "iniciar")
        echo "<h3>Iniciant Servei DHCP...</h3>"
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dhcp iniciar) </pre> <br>"
        ;;
    "aturar")
        echo "<h3>Aturant Servei DHCP...</h3>"
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dhcp aturar) </pre> <br>"
        ;;
    "configurar")
        accio=$(echo "$QUERY_STRING" | sed -n 's/^.*accio=\([^&]*\).*$/\1/p')
        case "$accio" in
            "guardar_conf")

                vid=$(echo "$QUERY_STRING" | sed -n 's/^.*vid=\([^&]*\).*$/\1/p')
                inici=$(echo "$QUERY_STRING" | sed -n 's/^.*inici=\([^&]*\).*$/\1/p')
                final=$(echo "$QUERY_STRING" | sed -n 's/^.*final=\([^&]*\).*$/\1/p')
                gateway=$(echo "$QUERY_STRING" | sed -n 's/^.*gateway=\([^&]*\).*$/\1/p')
                dns1=$(echo "$QUERY_STRING" | sed -n 's/^.*dns1=\([^&]*\).*$/\1/p')
                activat=$(echo "$QUERY_STRING" | sed -n 's/^.*activat=\([^&]*\).*$/\1/p')
                echo "<h3>Guardant configuració per VLAN $vid...</h3>"
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dhcp configurar guardar_conf $vid $inici $final $gateway $dns1 $activat)</pre> <br>"
                ;;
            "guardar_wifi_conf")
                echo "<h3>Guardant configuració WiFi...</h3>"
                ip=$(echo "$QUERY_STRING" | sed -n 's/^.*ip=\([^&]*\).*$/\1/p')
                ip=$(printf '%b' "${ip//%/\\x}")
                inici=$(echo "$QUERY_STRING" | sed -n 's/^.*inici=\([^&]*\).*$/\1/p')
                final=$(echo "$QUERY_STRING" | sed -n 's/^.*final=\([^&]*\).*$/\1/p')
                gateway=$(echo "$QUERY_STRING" | sed -n 's/^.*gateway=\([^&]*\).*$/\1/p')
                dns1=$(echo "$QUERY_STRING" | sed -n 's/^.*dns1=\([^&]*\).*$/\1/p')
                activat=$(echo "$QUERY_STRING" | sed -n 's/^.*activat=\([^&]*\).*$/\1/p')
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dhcp configurar guardar_wifi_conf $ip $inici $final $gateway $dns1 $activat)</pre> <br>"
                ;;
            *)
                echo "<p class='alert'>Acció invàlida. Falta [guardar_conf, guardar_wifi_conf]</p>"
                ;;
        esac
        ;;
    "estat" | *)
        echo "<h3>Configuració Activa DHCP</h3>"
        echo "<p style='color: #666; font-size: 14px;'>S'estructuren només les línies de configuració actives (es filtren els comentaris del sistema).</p>"
        echo "<div class='card' style='background: #1e1e1e; color: #d4d4d4; padding: 15px; border-radius: 8px; overflow-x: auto; font-family: monospace;'>"
        
        # Filtrem comentaris (#) i línies buides per veure la configuració bonica
        ESTAT_RAW=$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dhcp estat)
        echo "<pre style='margin: 0;'>"
        echo "$ESTAT_RAW" | grep -v '^[[:space:]]*#' | grep -v '^[[:space:]]*$'
        echo "</pre>"
        echo "</div>"
        
        # Mostrem també si el servei corre
        if echo "$ESTAT_RAW" | grep -q 'FUNCIONA'; then
            echo "<p style='margin-top: 15px;'><span class='card-status status-active'>SERVEI DHCP ACTIU</span></p>"
        fi
        ;;
esac

cat << EOF
        </div>
    </div>
</div>
</body>
</html>
EOF
