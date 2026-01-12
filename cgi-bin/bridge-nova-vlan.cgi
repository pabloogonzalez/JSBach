#!/bin/bash

source /usr/local/JSBach/conf/variables.conf


echo "Content-type: text/html; charset=utf-8"
echo ""

echo "<html><head><title>Crear VLAN</title>"
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

echo "<h2>Crear VLAN</h2>"
echo "<form action='/cgi-bin/bridge-guardar.cgi' method='get'>"
echo "<table>"
echo "<tr><th>Nom</th><th>VID</th><th>IP/Subxarxa</th><th>IP/PE</th></tr>"
echo "<tr>"
# Nom ara també més ample
echo "<td><input type='text' name='nom' value='' style='width: 250px;'></td>"
# VID només lectura
echo "<td><input type='text' name='vid' value='' ></td>"
# Camps IP més amplis
echo "<td><input type='text' class='ip' name='ipmasc' value=''></td>"
echo "<td><input type='text' class='ip' name='ippe' value=''></td>"
echo "</tr>"
echo "</table>"
echo "<button type='submit'>Crear</button>"
echo "</form>"

echo "</body></html>"

