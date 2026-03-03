#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
CONF_USUARIS="$DIR/$PROJECTE/$DIR_CONF/usuaris_wifi.conf"

echo "Content-type: text/html; charset=utf-8"
echo ""

# Obtenir usuari de la URL GET
USUARI=$(echo "$QUERY_STRING" | sed -n 's/^.*usuario=\([^&]*\).*$/\1/p')

if [ -n "$USUARI" ]; then
    # Escape special chars to avoid sed errors
    USUARI_ESC=$(echo "$USUARI" | sed 's/[.[\*^$]/\\&/g')
    
    # Esborrar l'usuari de l'arxiu (borra la línia que comenci per "Usuari;")
    if sed -i "/^$USUARI_ESC;/d" "$CONF_USUARIS"; then
        MSG="<div class='alert' style='color:green;'>L'usuari <b>$USUARI</b> ha estat eliminat correctament.</div>"
    else
        MSG="<div class='alert' style='color:red;'>Error al suprimir l'usuari.</div>"
    fi
else
    MSG="<div class='alert' style='color:red;'>No s'ha especificat cap usuari.</div>"
fi

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="2;url=/cgi-bin/portal-usuaris.cgi" />
    <title>Eliminant...</title>
    <link rel="stylesheet" href="/style.css">
    <style> body { font-family: sans-serif; padding: 40px; text-align: center; } </style>
</head>
<body>
    <h2>Processant...</h2>
    $MSG
    <p>Redirigint al portal en 2 segons...</p>
</body>
</html>
EOF
