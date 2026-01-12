#!/bin/bash

source /usr/local/JSBach/conf/variables.conf


echo "Content-type: text/html; charset=utf-8"
echo ""


int=$(echo "$QUERY_STRING" | sed -n 's/^.*int=\([^&]*\).*$/\1/p')

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

VLAN_DATA="$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge configurar mostrar bridge)"
linia_int=$(echo "$VLAN_DATA" | grep -E "^${int};")
VLAN_UNTAG=$(echo "$linia_int"|cut -d';' -f2)
if [[ -z "$VLAN_UNTAG" ]]; then
	   VLAN_UNTAG=0
fi
VLAN_TAG=$(echo "$linia_int"|cut -d';' -f3)
if [[ -z "$VLAN_TAG" ]]; then
	   VLAN_TAG=0
fi

echo "<h2>Modificar Tag-Untag</h2>"
echo "<form action='/cgi-bin/bridge-guardar-taguntag.cgi' method='get'>"
echo "<table>"
echo "<tr><th>Interfaç</th><th>Untag</th><th>Tag</th></tr>"
echo "<tr>"


echo "<td><input type='text' name='int' value='$int' style='width: 250px;' readonly></td>"   
echo "<td><input type='text' class='untag' name='untag' value='$VLAN_UNTAG'></td>"
echo "<td><input type='text' class='tag' name='tag' value='$VLAN_TAG'></td>"
echo "</tr>"
echo "</table>"
echo "<button type='submit' class='btn'>Guardar</button>"
echo "</form>"

echo "</div>" # End card
echo "</div>" # End container
echo "</body></html>"

