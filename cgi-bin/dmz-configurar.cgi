#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
source $DIR/$DIR_PROJECTE/$DIR_CONF/$IFWAN_CONF
source $DIR/$DIR_PROJECTE/$DIR_SCRIPTS/funcions

echo "Content-type: text/html; charset=utf-8"
echo ""

VLAN_DATA="$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge mostrar bridge)"

/bin/cat << EOM
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Configuració DMZ</title>
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
        <a href="/cgi-bin/dmz.cgi" class="nav-link active">DMZ</a>
    </div>
</nav>

<div class="container">
    <div class="card">
        <div class="card-header">
            <h2 class="card-title">Regles de Desmilitarització (DMZ)</h2>
        </div>
        <div class="card-body">
            
            <table class="table" style="margin-bottom: 24px;">
                <thead>
                    <tr>
                        <th>Port Extern</th>
                        <th>Protocol</th>
                        <th>Host Intern Destí (IP)</th>
                        <th style="text-align: right;">Accions</th>
                    </tr>
                </thead>
                <tbody>
EOF

DMZ_OP=0
IFS=$'\n'
for iface in $($DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli dmz configurar mostrar); do
    PORT=$(echo "$iface"|cut -d';' -f1)
    PROTO=$(echo "$iface"|cut -d';' -f2)
    IP_DMZ=$(echo "$iface"|cut -d';' -f3)

    if [ -n "$PORT" ]; then
        DMZ_OP=1
        echo "<tr>"
        echo "  <td style='font-weight: 600; color: var(--primary-color);'>Port $PORT</td>"
        echo "  <td style='text-transform: uppercase;'>$PROTO</td>"
        echo "  <td style='font-family: monospace; font-size: 14px;'>$IP_DMZ</td>"
        echo "  <td style='text-align: right;'>"
        echo "    <a href='/cgi-bin/dmz-eliminar.cgi?port=$PORT&proto=$PROTO&ipdmz=$IP_DMZ' class='btn btn-danger btn-sm'>Eliminar</a>"
        echo "  </td>"
        echo "</tr>"
    fi
done

if [ "$DMZ_OP" -eq 0 ]; then
    echo "<tr><td colspan='4' style='text-align: center; color: #666; padding: 20px;'>No hi ha cap port de la DMZ obert actualment.</td></tr>"
fi

cat << EOF
                </tbody>
            </table>

            <div style="display: flex; gap: 12px; justify-content: flex-end; margin-top: 24px;">
                <a href="/cgi-bin/dmz-nou-servei.cgi" class="btn btn-primary">Obrir Nou Port (Servei)</a>
                <a href="/cgi-bin/dmz.cgi" class="btn secondary">Tornar a DMZ</a>
            </div>
        </div>
    </div>
</div>

</body>
</html>
EOM
