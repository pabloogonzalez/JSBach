#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html"
echo ""

# --- Funció per obtenir interfícies de xarxa (excepte lo) ---
Interfaces_Ethernet() {
    for iface in $(ip -o link show | awk -F': ' '{print $2}'); do
        if [[ "$iface" != "lo" ]]; then
            echo "$iface"
        fi
    done
}

CONFIGURACIO=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli ifwan configurar mostrar)
conf_mode=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' '  -f1 )
conf_int=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' '  -f2 )
if [[ "$conf_mode" == "manual" ]] then
	conf_ip=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' '  -f3 )
	conf_masc=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' '  -f4 )
	conf_pe=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' '  -f5 )
	conf_dns=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' ' -f6 )
fi

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Configuració WAN</title>
    <link rel="stylesheet" href="/style.css">
    <script>
    function toggleManual() {
      const modeManual = document.getElementById("manual").checked;
      const manualSection = document.getElementById("manual-section");
      manualSection.style.display = modeManual ? "block" : "none";
    }
    window.addEventListener("DOMContentLoaded", toggleManual);
    </script>
</head>
<body>

<nav class="navbar">
    <a href="/cgi-bin/main.cgi" class="navbar-brand">
        <span>📶</span> Router Admin
    </a>
    <div class="nav-links">
        <a href="/cgi-bin/ifwan.cgi" class="nav-link active">WAN</a>
        <a href="/cgi-bin/enrutar.cgi" class="nav-link">Enrutament</a>
        <a href="/cgi-bin/bridge.cgi" class="nav-link">Bridge</a>
        <a href="/cgi-bin/tallafocs.cgi" class="nav-link">Tallafocs</a>
    </div>
</nav>

<div class="container">
    <div class="card">
        <div class="card-header">
            <h2 class="card-title">Configuració de la WAN</h2>
        </div>
        <div class="card-body">

<form action="/cgi-bin/ifwan-guardar.cgi" method="get">

<h3>Mode</h3>
EOF

dhcp_check=""
manual_check=""
if [[ "$conf_mode" == "dhcp" ]] then
    dhcp_check="checked"
else
    manual_check="checked"
fi

echo '<label><input type="radio" id="dhcp" name="mode" value="dhcp" onclick="toggleManual()" '$dhcp_check'> DHCP</label>'
echo '<div style="margin-top:8px"><label><input type="radio" id="manual" name="mode" value="manual" onclick="toggleManual()" '$manual_check'> Manual</label></div>'

cat << EOF
<h3 style="margin-top: 24px;">Interfície</h3>
EOF

for iface in $(Interfaces_Ethernet); do
    checked=""
    if [[ "$iface" == "$conf_int" ]]; then 
        checked="checked"
    fi
    echo "<div style='margin-bottom:8px'><label><input type='radio' name='int' id='$iface' value='$iface' $checked> $iface</label></div>"
done

cat << EOF
<div id="manual-section" style="display:none; margin-top: 24px; padding-top: 16px; border-top: 1px dashed #ddd;">
    <h3>Manual IP Config</h3>
    <label>IP:</label>
    <input type="text" name="ip" value="$conf_ip" placeholder="Ex: 192.168.1.100">
    
    <label>Màscara:</label>
    <input type="text" name="masc" value="$conf_masc" placeholder="Ex: 24">
    
    <label>Gateway:</label>
    <input type="text" name="pe" value="$conf_pe" placeholder="Ex: 192.168.1.1">
    
    <label>DNS:</label>
    <input type="text" name="dns" value="$conf_dns" placeholder="Ex: 8.8.8.8">
</div>

<div style="margin-top: 24px;">
    <button type="submit" class="btn">Guardar Canvis</button>
    <a href="/cgi-bin/ifwan.cgi" class="btn secondary">Cancel·lar</a>
</div>

</form>

        </div>
    </div>
</div>
</body>
</html>
EOF
