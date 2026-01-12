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
  <title>Guardant...</title>
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
<h2>Guardant canvis...</h2>
EOM


# Extreiem els valors del QUERY_STRING
int=$(echo "$QUERY_STRING" | sed -n 's/^.*int=\([^&]*\).*$/\1/p')
tag=$(echo "$QUERY_STRING" | sed -n 's/^.*tag=\([^&]*\).*$/\1/p')
untag=$(echo "$QUERY_STRING" | sed -n 's/^.*untag=\([^&]*\).*$/\1/p')

tag=$(urldecode "$tag")

echo "<pre>"
echo "$($RUTA bridge configurar guardar bridge $int $untag $tag)"
echo "</pre>"
echo "<p>Redirigint...</p>"
echo "</div></div>"

/bin/cat << EOM
</body>
</html>
EOM

