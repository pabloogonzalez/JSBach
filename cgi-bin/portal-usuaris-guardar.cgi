#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
CONF_USUARIS="$DIR/$PROJECTE/$DIR_CONF/usuaris_wifi.conf"

echo "Content-type: text/html; charset=utf-8"
echo ""

# Llegir dades POST
if [ "$REQUEST_METHOD" = "POST" ]; then
    if [ "$CONTENT_LENGTH" -gt 0 ]; then
        read -n $CONTENT_LENGTH POST_DATA
    fi
fi

# Funció per descodificar URL
url_decode() {
    local url_encoded="${1//+/ }"
    printf '%b' "${url_encoded//%/\\x}"
}

USER_ENC=$(echo "$POST_DATA" | grep -o 'usuario=[^&]*' | cut -d= -f2)
PASS_ENC=$(echo "$POST_DATA" | grep -o 'password=[^&]*' | cut -d= -f2)

USUARI=$(url_decode "$USER_ENC")
PASSWORD=$(url_decode "$PASS_ENC")

# Verificar si no estão buits
if [ -n "$USUARI" ] && [ -n "$PASSWORD" ]; then
    # Comprovar que no existeixi
    if grep -q "^$USUARI;" "$CONF_USUARIS" 2>/dev/null; then
        MSG="<div class='alert' style='color:red;'>L'usuari ja existeix.</div>"
    else
        echo "$USUARI;$PASSWORD" >> "$CONF_USUARIS"
        MSG="<div class='alert' style='color:green;'>Usuari guardat correctament.</div>"
    fi
else
    MSG="<div class='alert' style='color:red;'>Dades invàlides.</div>"
fi

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="2;url=/cgi-bin/portal-usuaris.cgi" />
    <title>Desant...</title>
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
