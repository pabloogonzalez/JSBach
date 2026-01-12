#!/bin/bash

# Load configuration
source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

# Handle actions
accio=$(echo "$QUERY_STRING" | sed -n 's/^.*accio=\([^&]*\).*$/\1/p')
protocol=$(echo "$QUERY_STRING" | sed -n 's/^.*protocol=\([^&]*\).*$/\1/p')
port=$(echo "$QUERY_STRING" | sed -n 's/^.*port=\([^&]*\).*$/\1/p')

if [ "$accio" == "afegir" ] && [ -n "$protocol" ] && [ -n "$port" ]; then
    RESULTAT=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs configurar afegir_port_wls "$protocol" "$port")
elif [ "$accio" == "eliminar" ] && [ -n "$protocol" ] && [ -n "$port" ]; then
    RESULTAT=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs configurar eliminar_port_wls "$protocol" "$port")
fi

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestió de Ports - Tallafocs</title>
    <link rel="stylesheet" href="/style.css">
    <style>
        .port-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px;
            border-bottom: 1px solid #eee;
        }
        .port-item:last-child {
            border-bottom: none;
        }
        .port-info {
            display: flex;
            gap: 16px;
        }
        .port-proto {
            font-weight: 600;
            color: #1a73e8;
            text-transform: uppercase;
            width: 40px;
        }
        .port-num {
            font-weight: 500;
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
            <h2 class="card-title">Gestió de Ports Permesos (Whitelist)</h2>
        </div>
        <div class="card-body">

            $(if [ -n "$RESULTAT" ]; then
                echo "<div class='alert' style='background: #e8f0fe; color: #1967d2; padding: 12px; border-radius: 4px; margin-bottom: 20px;'>$RESULTAT</div>"
            fi)

            <form action="tallafocs-ports.cgi" method="GET" class="card" style="box-shadow: none; border: 1px solid #eee; background: #f9f9f9; padding: 20px; margin-bottom: 24px;">
                <input type="hidden" name="accio" value="afegir">
                <div style="display: grid; grid-template-columns: 1fr 1fr auto; gap: 16px; align-items: end;">
                    <div>
                        <label style="display: block; margin-bottom: 8px; font-weight: 500;">Protocol</label>
                        <select name="protocol" class="form-control" style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px;">
                            <option value="tcp">TCP</option>
                            <option value="udp">UDP</option>
                        </select>
                    </div>
                    <div>
                        <label style="display: block; margin-bottom: 8px; font-weight: 500;">Número de Port</label>
                        <input type="number" name="port" class="form-control" placeholder="Ex: 80" required style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px;">
                    </div>
                    <button type="submit" class="btn">Afegir Port</button>
                </div>
            </form>

            <div class="card" style="box-shadow: none; border: 1px solid #eee;">
                <div class="card-header" style="background: #f5f5f5; padding: 12px 16px;">
                    <h3 style="margin: 0; font-size: 16px;">Llista de Ports Actuals</h3>
                </div>
                <div>
EOF

while read linia; do
    if [[ ! $linia =~ ^# ]] && [[ -n $linia ]]; then
        proto=$(echo "$linia" | cut -d';' -f1)
        num=$(echo "$linia" | cut -d';' -f2)
        
        echo "<div class='port-item'>"
        echo "  <div class='port-info'>"
        echo "    <span class='port-proto'>$proto</span>"
        echo "    <span class='port-num'>$num</span>"
        echo "  </div>"
        echo "  <a href='tallafocs-ports.cgi?accio=eliminar&protocol=$proto&port=$num' class='btn secondary' style='color: #d93025; border-color: #d93025; padding: 4px 12px; font-size: 13px;'>Eliminar</a>"
        echo "</div>"
    fi
done < "$DIR/$PROJECTE/$DIR_CONF/$PORTS_WLS"

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
