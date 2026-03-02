#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
WIFI_CONF="wifi.conf"
CONF_FILE="$DIR/$PROJECTE/$DIR_CONF/$WIFI_CONF"

echo "Content-type: text/html; charset=utf-8"
echo ""

# Llegir la configuració actual si existeix
WIFI_IFACE=""
WIFI_SSID=""
WIFI_PASSWD=""

if [ -f "$CONF_FILE" ]; then
    source "$CONF_FILE"
fi

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Configuració WiFi</title>
    <link rel="stylesheet" href="/style.css">
</head>
<body>

<nav class="navbar">
    <a href="/cgi-bin/main.cgi" class="navbar-brand">
        <span>📶</span> Router Admin
    </a>
    <div class="nav-links">
        <a href="/cgi-bin/ifwan.cgi" class="nav-link">WAN</a>
        <a href="/cgi-bin/wifi.cgi" class="nav-link active">WiFi</a>
        <a href="/cgi-bin/enrutar.cgi" class="nav-link">Enrutament</a>
        <a href="/cgi-bin/bridge.cgi" class="nav-link">Bridge</a>
        <a href="/cgi-bin/tallafocs.cgi" class="nav-link">Tallafocs</a>
        <a href="/cgi-bin/dmz.cgi" class="nav-link">DMZ</a>
        <a href="/cgi-bin/ebtables.cgi" class="nav-link">Ebtables</a>
    </div>
</nav>

<div class="container">
    <div class="card">
        <div class="card-header">
            <h2 class="card-title">Configurar Zona WiFi</h2>
        </div>
        <div class="card-body">

<form action="/cgi-bin/wifi-guardar.cgi" method="get">

    <div style="margin-bottom: 16px;">
        <label style="display: block; margin-bottom: 8px; font-weight: 500;">Interfície (Targeta Inalàmbrica):</label>
        <input type="text" name="iface" value="$WIFI_IFACE" placeholder="Ex: wlan0" required style="width: 100%; max-width: 300px; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
        <p style="font-size: 13px; color: #666; margin-top: 4px;">Escriu el nom de la interfície. Pots comprovar les teves interfícies desant ifconfig al terminal.</p>
    </div>

    <div style="margin-bottom: 16px;">
        <label style="display: block; margin-bottom: 8px; font-weight: 500;">Nom de la xarxa (SSID):</label>
        <input type="text" name="ssid" value="$WIFI_SSID" placeholder="Ex: ElMeuRouter" required style="width: 100%; max-width: 300px; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
    </div>

    <div style="margin-bottom: 16px;">
        <label style="display: block; margin-bottom: 8px; font-weight: 500;">Contrasenya (WPA2):</label>
        <input type="text" name="password" value="$WIFI_PASSWD" placeholder="Mínim 8 caràcters" required style="width: 100%; max-width: 300px; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
    </div>

    <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid #eee;">
        <button type="submit" class="btn">Guardar Canvis</button>
        <a href="/cgi-bin/wifi.cgi" class="btn secondary">Cancel·lar</a>
    </div>

</form>

        </div>
    </div>
</div>

</body>
</html>
EOF
