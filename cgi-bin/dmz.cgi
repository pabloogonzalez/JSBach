#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

comand=$(echo "$QUERY_STRING" | sed -n 's/^.*comand=\([^&]*\).*$/\1/p')

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestió DMZ</title>
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
        <a href="/cgi-bin/bridge.cgi" class="nav-link">Bridge</a>
        <a href="/cgi-bin/tallafocs.cgi" class="nav-link">Tallafocs</a>
        <a href="/cgi-bin/dmz.cgi" class="nav-link active">DMZ</a>
        <a href="/cgi-bin/ebtables.cgi" class="nav-link">Ebtables</a>
    </div>
</nav>

<div class="container">
    <div class="card">
        <div class="card-header">
            <h2 class="card-title">Gestió de la DMZ (Port Forwarding)</h2>
        </div>
        <div class="card-body">
EOF

if [ -n "$comand" ]; then
    echo "<div class='alert' style='background: #e0f2f1; color: #00796b; padding: 12px; border-radius: 4px; margin-bottom: 20px;'>"
    echo "  <strong>Acció realitzada:</strong> $comand<br>"
    echo "  <pre style='margin-top:8px; font-size: 12px;'>$($DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli dmz $comand)</pre>"
    echo "</div>"
fi

echo "<h3>Estat de la DMZ</h3>"
echo "<div class='card' style='box-shadow: none; border: 1px solid #eee; background: #f9f9f9; padding: 20px; margin-bottom: 24px;'>"
$DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli dmz estat
echo "</div>"

cat << EOF
            <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid #eee; display: flex; gap: 12px; flex-wrap: wrap;">
                <a href="/cgi-bin/dmz.cgi?comand=iniciar" class="btn">Iniciar DMZ</a>
                <a href="/cgi-bin/dmz.cgi?comand=aturar" class="btn secondary" style="color: #d93025; border-color: #d93025;">Aturar DMZ</a>
                <a href="/cgi-bin/dmz-configurar.cgi" class="btn secondary">Configurar Regles</a>
            </div>
        </div>
    </div>
</div>

</body>
</html>
EOF

