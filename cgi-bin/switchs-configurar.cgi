#!/bin/bash

# Load configuration
source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo "Cache-Control: no-cache, no-store, must-revalidate"
echo "Pragma: no-cache"
echo "Expires: 0"
echo ""

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="1; url=/cgi-bin/switchs.cgi">
    <title>Configuració Switchs</title>
    <link rel="stylesheet" href="/style.css">
</head>
<body>

<div class="container" style="text-align:center; margin-top:50px;">
    <div class="card">
        <div class="card-body">
            <h3>Processant acció...</h3>
            <div class="loader" style="margin: 20px auto;"></div>
            <pre style="background:#f5f5f5; padding:10px; border-radius:4px; text-align:left;">
EOF

# Parse Query String
accio=$(echo "$QUERY_STRING" | sed -n 's/^.*accio=\([^&]*\).*$/\1/p')
nom=$(echo "$QUERY_STRING" | sed -n 's/^.*nom=\([^&]*\).*$/\1/p' | sed 's/+/ /g' | sed 's/%20/ /g')
ip=$(echo "$QUERY_STRING" | sed -n 's/^.*ip=\([^&]*\).*$/\1/p')
user=$(echo "$QUERY_STRING" | sed -n 's/^.*user=\([^&]*\).*$/\1/p')
pass=$(echo "$QUERY_STRING" | sed -n 's/^.*pass=\([^&]*\).*$/\1/p')

# Execute Command via Client
# Usage: client_srv_cli switchs configurar [eliminar|afegir] [args...]
if [ "$accio" == "eliminar" ]; then
    $DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli switchs configurar eliminar "$nom" "$ip"
elif [ "$accio" == "afegir" ]; then
    $DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli switchs configurar afegir "$nom" "$ip" "$user" "$pass"
else
    echo "Acció desconeguda: $accio"
fi

cat << EOF
            </pre>
            <p><a href="/cgi-bin/switchs.cgi">Tornar si no redirigeix automàticament...</a></p>
        </div>
    </div>
</div>

</body>
</html>
EOF
