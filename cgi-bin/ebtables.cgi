#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

# Parse Query String
action=$(echo "$QUERY_STRING" | sed -n 's/^.*action=\([^&]*\).*$/\1/p')
iface=$(echo "$QUERY_STRING" | sed -n 's/^.*iface=\([^&]*\).*$/\1/p')

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestió Ebtables (L2)</title>
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
        <a href="/cgi-bin/dmz.cgi" class="nav-link">DMZ</a>
        <a href="/cgi-bin/ebtables.cgi" class="nav-link active">Ebtables</a>
    </div>
</nav>

<div class="container">
    <div class="card">
        <div class="card-header">
            <h2 class="card-title">Gestió Tallafocs L2 (Ebtables)</h2>
        </div>
        <div class="card-body">
            <div style="margin-bottom: 20px;">
                <a href="/cgi-bin/tallafocs.cgi" class="btn secondary">← Tornar a Tallafocs</a>
            </div>
EOF

# Handle Action
if [ "$action" == "toggle" ] && [ -n "$iface" ]; then
    echo "<div class='alert'>"
    echo "Processing $iface..."
    $DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli tallafocs ebtables_toggle $iface
    echo "</div>"
fi

# Show Status
$DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli tallafocs ebtables_status

cat << EOF
        </div>
    </div>
</div>

</body>
</html>
EOF
