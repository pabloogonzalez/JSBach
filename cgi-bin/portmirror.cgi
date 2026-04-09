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
    <title>Port Mirroring</title>
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
        <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
            <h2 class="card-title">Estat i Control de Port Mirroring</h2>
            <div>
                <a href="/cgi-bin/portmirror.cgi?comand=iniciar" class="btn btn-primary">Iniciar</a>
                <a href="/cgi-bin/portmirror.cgi?comand=aturar" class="btn btn-danger">Aturar</a>
                <a href="/cgi-bin/portmirror.cgi?comand=estat" class="btn secondary">Estat</a>
                <a href="/cgi-bin/portmirror-configurar.cgi" class="btn secondary">Configuració</a>
            </div>
        </div>
        <div class="card-body">
EOF

case $comand in
    iniciar)
        echo "<h3>Iniciant Port Mirroring...</h3>"
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portmirror iniciar) </pre><br>"
        ;;
    aturar)
        echo "<h3>Aturant Port Mirroring...</h3>"
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portmirror aturar) </pre><br>"
        ;;
    configurar)        
        argument=$(echo "$QUERY_STRING" | sed -n 's/^.*argument=\([^&]*\).*$/\1/p')
        case $argument in
            canviar_interface_sensor)
                interface_sensor=$(echo "$QUERY_STRING" | sed -n 's/^.*interface_sensor=\([^&]*\).*$/\1/p')
                echo "<h3>Actualitzant interfaç sensor: $interface_sensor</h3>"
                echo "<pre>$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror configurar canviar_interface_sensor $interface_sensor) </pre><br>"
                ;;
            modificar_interfaces_lan)
                echo "<h3>Actualitzant interfícies monitoritzades...</h3>"
                LLISTA_INTEFACES=$(ip link show | grep "^[0-9]:" | cut -d ":" -f 2 | cut -d "@" -f 1)
                INTERFACES_LAN=""
                for interface in $LLISTA_INTEFACES
                do
                    if echo "$QUERY_STRING" | grep -q "$interface"; then
                        INTERFACES_LAN+="$interface,"
                    fi
                done
                echo "<pre>$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror configurar modificar_interfaces_lan $INTERFACES_LAN) </pre><br>"
                ;;
        esac
        ;;
    mostrar)
        argument=$(echo "$QUERY_STRING" | sed -n 's/^.*argument=\([^&]*\).*$/\1/p')
        case $argument in       
            interface_sensor)
                echo "<h3>Interfaç Sensor</h3>"
                echo "<pre>$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror mostrar interface_sensor) </pre><br>"
                ;;
            interfaces_lan)
                echo "<h3>Interfaces Monitoritzades</h3>"
                echo "<pre>$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror mostrar interfaces_lan) </pre><br>"
                ;;
            tot)
                echo "<h3>Configuració Completa</h3>"
                echo "<pre>$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror mostrar tot) </pre><br>"
                ;;
        esac
        ;;
    estat | *)
        echo "<h3>Estat Actual</h3>"
        echo "<pre>$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror estat) </pre><br>"
        ;;
esac

retorn=$(echo "$QUERY_STRING" | sed -n 's/^.*retorn=\([^&]*\).*$/\1/p')
if [ "$retorn" != "" ]; then
    echo "<br><br><a href='/cgi-bin/$retorn' class='btn secondary'>Tornar</a>"
fi 

cat << EOF
        </div>
    </div>
</div>
</body>
</html>
EOF
