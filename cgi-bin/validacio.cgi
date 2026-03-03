#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
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

# Extreure usuari i contrasenya
USER_ENC=$(echo "$POST_DATA" | grep -o 'usuario=[^&]*' | cut -d= -f2)
PASS_ENC=$(echo "$POST_DATA" | grep -o 'password=[^&]*' | cut -d= -f2)

USUARI=$(url_decode "$USER_ENC")
PASSWORD=$(url_decode "$PASS_ENC")

# Comprovar credencials a l'arxiu de configuració
CONF_USUARIS="$DIR/$PROJECTE/$DIR_CONF/usuaris_wifi.conf"
VALID=false

if [ -f "$CONF_USUARIS" ]; then
    while IFS=';' read -r conf_user conf_pass; do
        # Eliminar posibles retorns de carro
        conf_user=$(echo "$conf_user" | tr -d '\r')
        conf_pass=$(echo "$conf_pass" | tr -d '\r')
        
        if [ "$USUARI" == "$conf_user" ] && [ "$PASSWORD" == "$conf_pass" ]; then
            VALID=true
            break
        fi
    done < "$CONF_USUARIS"
fi

cat << EOM
<html>
<head>
  <meta charset="utf-8">
  <title>Portal Captiu - JSBach</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
EOM
cat $DIR/$PROJECTE/$DIR_CGI/$CSS_CGI_BIN 2>/dev/null
cat << EOM
  <style>
    body { font-family: Arial, sans-serif; background: #f4f6f9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
    .card { background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; max-width: 400px; width: 90%; }
    h2 { color: #2c3e50; }
    p { color: #555; }
    .btn { display: inline-block; padding: 12px 20px; background: #3498db; color: white; text-decoration: none; border-radius: 6px; margin-top: 20px; width: 100%; box-sizing: border-box; }
    .btn:hover { background: #2980b9; }
    .success { color: #27ae60; }
    .error { color: #e74c3c; }
  </style>
</head>
<body>
  <div class="card">
EOM

if [ "$VALID" = true ]; then
    IP_CLIENT="$REMOTE_ADDR"
    
    # Obtenir MAC a partir de la taula ARP
    MAC_CLIENT=$(arp -n | grep -w "$IP_CLIENT" | awk '{print $3}')
    
    if [ -n "$MAC_CLIENT" ] && [ "$MAC_CLIENT" != "incomplete" ]; then
        # Cercar l'ID de la VLAN basant-se en la IP (ex: 10.0.3.50 -> 10.0.3.0/24)
        IP_BASE=$(echo "$IP_CLIENT" | cut -d'.' -f1,2,3)
        VID=$(grep ";$IP_BASE\.0/" "$DIR/$PROJECTE/$DIR_CONF/$BRIDGE_CONF" | cut -d';' -f2)
        
        if [ -n "$VID" ]; then
            # Cridar el backend per afegir a la llista blanca d'IPs (tallafocs)
            $DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli tallafocs configurar afegir_ip_wls "$VID" "$IP_CLIENT" "$MAC_CLIENT" >/dev/null 2>&1
            
            echo "    <h2 class='success'>¡Connexió Exitosa!</h2>"
            echo "    <p>T'has autenticat correctament.</p>"
            echo "    <p>IP: <strong>$IP_CLIENT</strong><br>MAC: <strong>$MAC_CLIENT</strong></p>"
            echo "    <p>Ja tens accés a la xarxa.</p>"
        else
            echo "    <h2 class='error'>Error Intern</h2>"
            echo "    <p>No s'ha pogut determinar la VLAN per a la IP $IP_CLIENT.</p>"
            echo "    <p>Si us plau, contacta amb l'administrador.</p>"
        fi
    else
        echo "    <h2 class='error'>Error de Xarxa</h2>"
        echo "    <p>No s'ha pogut trobar la teva adreça física (MAC).</p>"
        echo "    <p>Estàs directament connectat a la xarxa?</p>"
    fi
else
    echo "    <h2 class='error'>Credencials Incorrectes</h2>"
    echo "    <p>L'usuari o la contrasenya no són vàlids.</p>"
    echo "    <a href='/portal_captiu/validacio.html' class='btn'>Tornar-ho a intentar</a>"
fi

cat << EOM
  </div>
</body>
</html>
EOM