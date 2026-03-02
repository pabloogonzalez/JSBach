#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

# Obtenir parametres
iface=$(echo "$QUERY_STRING" | sed -n 's/^.*iface=\([^&]*\).*$/\1/p' | sed 's/%20/ /g')
ssid=$(echo "$QUERY_STRING" | sed -n 's/^.*ssid=\([^&]*\).*$/\1/p' | sed 's/%20/ /g')
password=$(echo "$QUERY_STRING" | sed -n 's/^.*password=\([^&]*\).*$/\1/p' | sed 's/%20/ /g')

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="2;url=/cgi-bin/wifi.cgi" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guardant WiFi...</title>
    <link rel="stylesheet" href="/style.css">
</head>
<body>

<nav class="navbar">
    <a href="/cgi-bin/main.cgi" class="navbar-brand">
        <span>📶</span> Router Admin
    </a>
</nav>

<div class="container">
    <div class="card">
        <div class="card-header">
            <h2 class="card-title">Configuració</h2>
        </div>
        <div class="card-body">
            <h3>Guardant valors...</h3>
            <pre>
EOF

$DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli wifi configurar "$iface" "$ssid" "$password"

cat << EOF
            </pre>
            <p>Redirigint a la Gestió WiFi...</p>
            <a href="/cgi-bin/wifi.cgi" class="btn">Tornar manualment</a>
        </div>
    </div>
</div>

</body>
</html>
EOF
