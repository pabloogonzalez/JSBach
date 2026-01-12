#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

# Get command from query string
comand=$(echo "$QUERY_STRING" | sed -n 's/^.*comand=\([^&]*\).*$/\1/p')

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestió WAN</title>
    <link rel="stylesheet" href="/style.css">
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
            <h2 class="card-title">Gestió WAN</h2>
        </div>
        <div class="card-body">
EOF

if [ -n "$comand" ]; then
    echo "<h3>Resultat: $comand</h3>"
    echo "<pre>"
    $DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli ifwan $comand
    echo "</pre>"
fi

echo "<h3>Estat Actual</h3>"
echo "<div>"
$DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli ifwan estat
echo "</div>"

cat << EOF
            <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid #eee;">
                <a href="/cgi-bin/ifwan.cgi?comand=iniciar" class="btn">Iniciar</a>
                <a href="/cgi-bin/ifwan.cgi?comand=aturar" class="btn secondary" style="color: #d93025; border-color: #d93025;">Aturar</a>
                <a href="/cgi-bin/ifwan-configurar.cgi" class="btn secondary">Configurar</a>
            </div>
        </div>
    </div>
</div>

</body>
</html>
EOF
