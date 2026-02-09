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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestió de Switchs</title>
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
        <a href="/cgi-bin/ebtables.cgi" class="nav-link">Ebtables</a>
        <a href="/cgi-bin/switchs.cgi" class="nav-link active">Switchs</a>
    </div>
</nav>

<div class="container">
    <div class="card">
        <div class="card-header">
            <h2 class="card-title">Infraestructura de Xarxa (Switchs)</h2>
            <a href="/cgi-bin/switchs-nou.cgi" class="btn small">Afegir Switch</a>
        </div>
        <div class="card-body">
            
            <table class="table">
              <thead>
                <tr>
                  <th>Nom del Switch</th>
                  <th>Adreça IP</th>
                  <th>Estat</th>
                  <th>Accions</th>
                </tr>
              </thead>
              <tbody>
EOF

# Get status from script
# Output format: "nom ip ESTAT"
$DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli switchs estat | while read -r nom ip estat; do
    echo "<tr>"
    echo "<td><strong>$nom</strong></td>"
    
    if [[ "$estat" == "FUNCIONA" ]]; then
        echo "<td><a href='http://$ip' target='_blank' style='color:#1a73e8; text-decoration:none;'>$ip ↗</a></td>"
        echo "<td><span class='badge badge-success'>ACTIU</span></td>"
    else
        echo "<td>$ip</td>"
        echo "<td><span class='badge badge-danger'>NO RESPON</span></td>"
    fi
    
    echo "<td>"
    echo "<div style='display:flex; gap:8px;'>"
    echo "  <a href='switchs-configurar.cgi?accio=eliminar&nom=$nom&ip=$ip' class='btn btn-danger btn-sm' onclick=\"return confirm('Segur que vols eliminar aquest switch?');\">Eliminar</a>"
    # Placeholder for future "mac table" feature if needed, though not in dashboard requirement yet
    # echo "  <a href='switchs-configurar.cgi?accio=taula_mac&ip=$ip' class='btn btn-secondary btn-sm'>MACs</a>"
    echo "</div>"
    echo "</td>"
    echo "</tr>"
done

cat << EOF
              </tbody>
            </table>
            
            <div style="margin-top: 20px; font-size: 0.9em; color: #666;">
                <p>Nota: L'estat es verifica mitjançant PING (timeout 1s).</p>
            </div>
        </div>
    </div>
</div>

</body>
</html>
EOF
