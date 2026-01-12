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
    <title>Gestió Bridge</title>
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
        <a href="/cgi-bin/bridge.cgi" class="nav-link active">Bridge</a>
        <a href="/cgi-bin/tallafocs.cgi" class="nav-link">Tallafocs</a>
    </div>
</nav>

<div class="container">
    <div class="card">
        <div class="card-header">
            <h2 class="card-title">Configuració Bridge i VLANs</h2>
        </div>
        <div class="card-body">
EOF

if [ -n "$comand" ]; then
    echo "<h3>Resultat: $comand</h3>"
    echo "<pre>"
    $DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli bridge $comand
    echo "</pre>"
fi


echo "<h3>Estat Actual</h3>"
echo "<div>"
$DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli bridge estat
echo "</div>"

cat << EOF
            <h3 style="margin-top: 32px;">Gestió del Servei</h3>
            <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px; padding-bottom: 24px; border-bottom: 1px solid #eee;">
                <a href="/cgi-bin/bridge.cgi?comand=iniciar" class="btn">Iniciar Bridge</a>
                <a href="/cgi-bin/bridge.cgi?comand=aturar" class="btn secondary" style="color: #d93025; border-color: #d93025;">Aturar Bridge</a>
            </div>

            <h3 style="margin-top: 24px;">Configuració Avançada</h3>
            <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px;">
                <a href="/cgi-bin/bridge-configurar.cgi" class="btn secondary">Gestionar VLANs</a>
                <a href="/cgi-bin/bridge-configurar-taguntag.cgi" class="btn secondary">Tag/Untag Interfícies</a>
            </div>
        </div>
    </div>
</div>

</body>
</html>
EOF
