#!/bin/bash

source /usr/local/JSBach/conf/variables.conf


echo "Content-type: text/html; charset=utf-8"
echo ""


QUERY_STRING=${QUERY_STRING:-$1}  
VID=$(echo "$QUERY_STRING" | sed -n 's/.*vid=\([0-9]*\).*/\1/p')

echo "<html><head><title>Esborrar  VLAN</title>"
echo "<meta charset='utf-8'>"
echo "<style>
body { font-family: sans-serif; margin: 20px; background: #f6f6f6; }
h2 { background: #ddd; padding: 6px; }
table { border-collapse: collapse; margin-bottom: 20px; width: 60%; }
td, th { border: 1px solid #999; padding: 6px 10px; }
th { background: #f0f0f0; text-align: left; }
input { width: 95%; padding: 6px; font-size: 14px; }
input.ip { width: 200px; }  /* Amplada específica per IP */
button { padding: 6px 12px; margin-top: 10px; font-size: 14px; }
</style>"
echo "</head><body>"

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

echo "<h2>Esborrar VLAN</h2>"
echo "<form action='/cgi-bin/bridge-aplicar-esborrar.cgi' method='get'>"
echo "<table>"
echo "<tr><th>Nom</th><th>VID</th><th>IP/Subxarxa</th><th>IP/PE</th></tr>"
echo "<tr>"
# Nom ara també més ample
echo "<td><input type='text' name='nom' value='$nom' style='width: 250px;' readonly></td>"
# VID només lectura
echo "<td><input type='text' name='vid' value='$vid' readonly></td>"
# Camps IP més amplis
echo "<td><input type='text' class='ip' name='ipmasc' value='$subnet' readonly></td>"
echo "<td><input type='text' class='ip' name='ippe' value='$gw' readonly></td>"
echo "</tr>"
echo "</table>"
echo "<button type='submit'>Esborrar</button>"
echo "</form>"

echo "</body></html>"

