#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
RUTA="$DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli"

urldecode() {
    local data="${1//+/ }"      # Canvia + per espai
    printf '%b' "${data//%/\\x}" # Converteix %xx en caràcters
}


echo "Content-type: text/html; charset=utf-8"
echo ""


/bin/cat << EOM
<html>
<head>
  <meta charset="utf-8">
  <title>Esborrant...</title>
  <link rel="stylesheet" href="/style.css">
  <meta http-equiv="refresh" content="2;url=/cgi-bin/bridge.cgi">
</head>
<body>
<nav class="navbar">
    <a href="/cgi-bin/main.cgi" class="navbar-brand">
        <span>📶</span> Router Admin
    </a>
</nav>
<div class="container">
<div class="card">
<h2>Esborrant VLAN...</h2>
EOM

# Extreiem els valors del QUERY_STRING
nom=$(echo "$QUERY_STRING" | sed -n 's/^.*nom=\([^&]*\).*$/\1/p')
vid=$(echo "$QUERY_STRING" | sed -n 's/^.*vid=\([^&]*\).*$/\1/p')
ipmasc=$(echo "$QUERY_STRING" | sed -n 's/^.*ipmasc=\([^&]*\).*$/\1/p')
ippe=$(echo "$QUERY_STRING" | sed -n 's/^.*ippe=\([^&]*\).*$/\1/p')


# Decodifiquem els valors
nom=$(urldecode "$nom")
ipmasc=$(urldecode "$ipmasc")
ippe=$(urldecode "$ippe")


echo "<pre>"
echo "$($RUTA bridge configurar esborrar vlan $vid)"
echo "</pre>"
echo "<p>Redirigint...</p>"
echo "</div></div>"

/bin/cat << EOM
</body>
</html>
EOM

