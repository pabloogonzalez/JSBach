#!/bin/bash


source /usr/local/JSBach/conf/variables.conf


echo "Content-type: text/html; charset=utf-8"
echo ""

PORT=$(echo "$QUERY_STRING" | sed -n 's/^.*port=\([^&]*\).*$/\1/p')
PROTO=$(echo "$QUERY_STRING" | sed -n 's/^.*proto=\([^&]*\).*$/\1/p')
IP_DMZ=$(echo "$QUERY_STRING" | sed -n 's/^.*ipdmz=\([^&]*\).*$/\1/p')

RESULTAT=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dmz configurar eliminar "$PORT" "$PROTO" "$IP_DMZ")

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Servei DMZ Eliminat</title>
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
    </div>
</nav>

<div class="container">
    <div class="card">
        <div class="card-header">
            <h2 class="card-title">Eliminar Servei DMZ</h2>
        </div>
        <div class="card-body">
            <div class="alert" style="background: #e0f2f1; color: #00796b; padding: 16px; border-radius: 4px; margin-bottom: 24px;">
                <h3 style="margin-top: 0; margin-bottom: 8px;">Eliminant Port \$PORT (\$PROTO) a la IP \$IP_DMZ</h3>
                <pre style="margin: 0; font-size: 13px; background: transparent; padding: 0;">\$RESULTAT</pre>
            </div>
            
            <div style="display: flex; gap: 12px; margin-top: 24px;">
                <a href="/cgi-bin/dmz-configurar.cgi" class="btn">Tornar a la Configuració DMZ</a>
            </div>
        </div>
    </div>
</div>

</body>
</html>
EOF
