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
    <title>Gestió de VLANs</title>
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
        <a href="/cgi-bin/bridge.cgi" class="nav-link active">Bridge</a>
        <a href="/cgi-bin/tallafocs.cgi" class="nav-link">Tallafocs</a>
        <a href="/cgi-bin/dmz.cgi" class="nav-link">DMZ</a>
        <a href="/cgi-bin/ebtables.cgi" class="nav-link">Ebtables</a>
    </div>
</nav>

<div class="container">
    <div class="card">
        <div class="card-header">
            <h2 class="card-title">Gestió de VLANs</h2>
        </div>
        <div class="card-body">

EOF

# Data retrieval
VLAN_DATA="$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge configurar mostrar vlan)"
mapfile -t VLANS <<< "$VLAN_DATA"

if [ "${#VLANS[@]}" -lt 2 ]; then
    echo "<div style='color: var(--danger-color); padding: 15px; border: 1px solid var(--danger-color); border-radius: 4px;'>"
    echo "<b>Error:</b> No hi ha prou VLANs definides al sistema."
    echo "</div>"
    echo "</div></div></div></body></html>"
    exit 0
fi

# -- VLAN ADMIN --
echo "<h3>VLAN Administració</h3>"
echo "<table>"
echo "<tr><th>Nom</th><th>VID</th><th>Subxarxa</th><th>Gateway</th><th style='width: 150px;'>Accions</th></tr>"
IFS=';' read -r nom vid subnet gw _ <<< "${VLANS[0]}"
echo "<tr><td>$nom</td><td>$vid</td><td>$subnet</td><td>$gw</td>"
echo "<td><a href='/cgi-bin/bridge-modificar.cgi?vid=$vid' class='btn secondary' style='padding: 4px 10px; font-size: 12px;'>Modificar</a></td></tr>"
echo "</table>"

# -- VLAN DMZ --
echo "<h3 style='margin-top: 30px;'>VLAN DMZ</h3>"
echo "<table>"
echo "<tr><th>Nom</th><th>VID</th><th>Subxarxa</th><th>Gateway</th><th style='width: 150px;'>Accions</th></tr>"
IFS=';' read -r nom vid subnet gw _ <<< "${VLANS[1]}"
echo "<tr><td>$nom</td><td>$vid</td><td>$subnet</td><td>$gw</td>"
echo "<td><a href='/cgi-bin/bridge-modificar.cgi?vid=$vid' class='btn secondary' style='padding: 4px 10px; font-size: 12px;'>Modificar</a></td></tr>"
echo "</table>"

# -- OTRAS VLANS --
echo "<h3 style='margin-top: 30px;'>Altres VLANs</h3>"
echo "<table>"
echo "<tr><th>Nom</th><th>VID</th><th>Subxarxa</th><th>Gateway</th><th style='width: 200px;'>Accions</th></tr>"

count=0
for ((i=2; i<${#VLANS[@]}; i++)); do
    line="${VLANS[$i]}"
    [ -z "$line" ] && continue
    count=$((count+1))
    IFS=';' read -r nom vid subnet gw _ <<< "$line"
    echo "<tr><td>$nom</td><td>$vid</td><td>$subnet</td><td>$gw</td>"
    echo "<td>"
    echo "<a href='/cgi-bin/bridge-modificar.cgi?vid=$vid' class='btn secondary' style='padding: 4px 10px; font-size: 12px; margin-right: 5px;'>Modificar</a>"
    echo "<a href='/cgi-bin/bridge-esborrar.cgi?vid=$vid' class='btn secondary' style='padding: 4px 10px; font-size: 12px; color: var(--danger-color); border-color: var(--danger-color);'>Esborrar</a>"
    echo "</td></tr>"
done

if [ "$count" -eq 0 ]; then
    echo "<tr><td colspan='5' style='text-align: center; color: #666;'>No hi ha VLANs addicionals configurades.</td></tr>"
fi
echo "</table>"

echo "<div style='margin-top: 24px; text-align: right;'>"
echo "<a href='/cgi-bin/bridge-nova-vlan.cgi' class='btn'>+ Crear Nova VLAN</a>"
echo "<a href='/cgi-bin/bridge.cgi' class='btn secondary' style='margin-left: 10px;'>Tornar al Bridge</a>"
echo "</div>"

cat << EOF
        </div>
    </div>
</div>
</body>
</html>
EOF
