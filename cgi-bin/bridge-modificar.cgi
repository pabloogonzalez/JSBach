#!/bin/bash

source /usr/local/JSBach/conf/variables.conf


echo "Content-type: text/html; charset=utf-8"
echo ""


QUERY_STRING=${QUERY_STRING:-$1}  
VID=$(echo "$QUERY_STRING" | sed -n 's/.*vid=\([0-9]*\).*/\1/p')

echo "<html><head><title>Modificar VLAN</title>"
echo "<meta charset='utf-8'>"
echo "<link rel='stylesheet' href='/style.css'>"
echo "</head><body>"

# Navbar
echo '<nav class="navbar">
    <a href="/cgi-bin/main.cgi" class="navbar-brand">
        <span>📶</span> Router Admin
    </a>
    <div class="nav-links">
        <a href="/cgi-bin/ifwan.cgi" class="nav-link">WAN</a>
        <a href="/cgi-bin/enrutar.cgi" class="nav-link">Enrutament</a>
        <a href="/cgi-bin/bridge.cgi" class="nav-link">Bridge</a>
        <a href="/cgi-bin/tallafocs.cgi" class="nav-link">Tallafocs</a>
    </div>
</nav>'

echo "<div class='container'>"
echo "<div class='card'>"

VLAN_DATA="$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge configurar mostrar vlan)"
mapfile -t VLANS <<< "$VLAN_DATA"

FOUND_LINE=""
for line in "${VLANS[@]}"; do
    IFS=';' read -r nom vid subnet gw _ <<< "$line"
    if [ "$vid" == "$VID" ]; then
        FOUND_LINE="$line"
        break
    fi
done

if [ -z "$FOUND_LINE" ]; then
    echo "<p><b>Error:</b> No s'ha trobat cap VLAN amb VID = $VID</p>"
    echo "</body></html>"
    exit 0
fi

IFS=';' read -r nom vid subnet gw _ <<< "$FOUND_LINE"

echo "<h2>Modificar VLAN</h2>"
echo "<form action='/cgi-bin/bridge-guardar.cgi' method='get'>"
echo "<table>"
echo "<tr><th>Nom</th><th>VID</th><th>IP/Subxarxa</th><th>IP/PE</th></tr>"
echo "<tr>"
# Nom ara també més ample

if [ "$vid" -lt "3" ]; then
     	echo "<td><input type='text' name='nom' value='$nom' style='width: 250px;' readonly></td>"   
else
	echo "<td><input type='text' name='nom' value='$nom' style='width: 250px;'></td>"
fi


# VID només lectura
echo "<td><input type='text' name='vid' value='$vid' readonly></td>"
# Camps IP més amplis
echo "<td><input type='text' class='ip' name='ipmasc' value='$subnet'></td>"
echo "<td><input type='text' class='ip' name='ippe' value='$gw'></td>"
echo "</tr>"
echo "</table>"
echo "<button type='submit' class='btn'>Guardar</button>"
echo "</form>"

echo "</div>" # End card
echo "</div>" # End container
echo "</body></html>"

