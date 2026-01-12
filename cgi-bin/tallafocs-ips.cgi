#!/bin/bash

# Load configuration
source /usr/local/JSBach/conf/variables.conf

# URL Decode function
urldecode() {
    local i="${1//%/\\x}"
    echo -e "${i//+/ }"
}

echo "Content-type: text/html; charset=utf-8"
echo ""

# Handle actions
extract_param() {
    echo "$QUERY_STRING" | grep -oE "(^|[&])$1=[^&]*" | cut -d= -f2
}

accio=$(urldecode "$(extract_param accio)")
vid=$(urldecode "$(extract_param vid)")
ip=$(urldecode "$(extract_param ip)")
mac=$(urldecode "$(extract_param mac)")

if [ "$accio" == "afegir" ] && [ -n "$vid" ] && [ -n "$ip" ] && [ -n "$mac" ]; then
    RESULTAT=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs configurar afegir_ip_wls "$vid" "$ip" "$mac")
elif [ "$accio" == "eliminar" ] && [ -n "$vid" ] && [ -n "$ip" ] && [ -n "$mac" ]; then
    RESULTAT=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs configurar eliminar_ip_wls "$vid" "$ip" "$mac")
fi

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestió d'IPs Privilegiades - Tallafocs</title>
    <link rel="stylesheet" href="/style.css">
    <style>
        .ip-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px;
            border-bottom: 1px solid #eee;
        }
        .ip-item:last-child {
            border-bottom: none;
        }
        .ip-info {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }
        .ip-vid {
            font-weight: 600;
            color: #1a73e8;
            width: 60px;
        }
        .ip-addr {
            font-weight: 500;
            width: 120px;
        }
        .ip-mac {
            color: #666;
            font-family: monospace;
        }
    </style>
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
        <a href="/cgi-bin/tallafocs.cgi" class="nav-link active">Tallafocs</a>
    </div>
</nav>

<div class="container">
    <div class="card">
        <div class="card-header">
            <h2 class="card-title">Gestió d'IPs amb Accés Sense Restriccions</h2>
        </div>
        <div class="card-body">

            $(if [ -n "$RESULTAT" ]; then
                echo "<div class='alert' style='background: #e8f0fe; color: #1967d2; padding: 12px; border-radius: 4px; margin-bottom: 20px;'>$RESULTAT</div>"
            fi)

            <form action="tallafocs-ips.cgi" method="GET" class="card" style="box-shadow: none; border: 1px solid #eee; background: #f9f9f9; padding: 20px; margin-bottom: 24px;">
                <input type="hidden" name="accio" value="afegir">
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr auto; gap: 16px; align-items: end;">
                    <div>
                        <label style="display: block; margin-bottom: 8px; font-weight: 500;">VLAN (VID)</label>
                        <select name="vid" class="form-control" style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px;">
EOF

# Get VLANs from bridge.conf
while read linia; do
    if [[ ! $linia =~ ^# ]] && [[ -n $linia ]]; then
        nom=$(echo "$linia" | cut -d';' -f1)
        vid_opt=$(echo "$linia" | cut -d';' -f2)
        echo "<option value='$vid_opt'>$nom (VID $vid_opt)</option>"
    fi
done < "$DIR/$PROJECTE/$DIR_CONF/$BRIDGE_CONF"

cat << EOF
                        </select>
                    </div>
                    <div>
                        <label style="display: block; margin-bottom: 8px; font-weight: 500;">Adreça IP</label>
                        <input type="text" name="ip" class="form-control" placeholder="Ex: 10.0.3.50" required style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px;">
                    </div>
                    <div>
                        <label style="display: block; margin-bottom: 8px; font-weight: 500;">Adreça MAC</label>
                        <input type="text" name="mac" class="form-control" placeholder="Ex: AA:BB:CC:DD:EE:FF" required style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px;">
                    </div>
                    <button type="submit" class="btn">Afegir Dispositiu</button>
                </div>
            </form>

            <div class="card" style="box-shadow: none; border: 1px solid #eee;">
                <div class="card-header" style="background: #f5f5f5; padding: 12px 16px;">
                    <h3 style="margin: 0; font-size: 16px;">Dispositius amb Accés Total</h3>
                </div>
                <div>
EOF

while read linia; do
    if [[ ! $linia =~ ^# ]] && [[ -n $linia ]]; then
        v=$(echo "$linia" | cut -d';' -f1)
        i=$(echo "$linia" | cut -d';' -f2)
        m=$(echo "$linia" | cut -d';' -f3)
        
        echo "<div class='ip-item'>"
        echo "  <div class='ip-info'>"
        echo "    <span class='ip-vid'>VID $v</span>"
        echo "    <span class='ip-addr'>$i</span>"
        echo "    <span class='ip-mac'>$m</span>"
        echo "  </div>"
        echo "  <a href='tallafocs-ips.cgi?accio=eliminar&vid=$v&ip=$i&mac=$m' class='btn secondary' style='color: #d93025; border-color: #d93025; padding: 4px 12px; font-size: 13px;'>Eliminar</a>"
        echo "</div>"
    fi
done < "$DIR/$PROJECTE/$DIR_CONF/$IPS_WLS"

cat << EOF
                </div>
            </div>

            <div style="margin-top: 24px; text-align: right;">
                <a href="/cgi-bin/tallafocs.cgi" class="btn secondary">Tornar al Tallafocs</a>
            </div>

        </div>
    </div>
</div>
</body>
</html>
EOF
