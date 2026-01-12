#!/bin/bash

# Load configuration
source /usr/local/JSBach/conf/variables.conf
source $DIR/$PROJECTE/$DIR_CONF/$CONF_IFWAN

# --- Funció per obtenir interfícies (sense lo, wan ni bridge) ---
Interfaces_Ethernet() {
    for iface in $(ip -o link show | awk -F': ' '{print $2}'); do
        if [[ "$iface" != "lo" ]] && [[ "$iface" != "$IFW_IFWAN" ]] && [[ $iface != br0* ]]; then
             echo "$iface"
        fi
    done
}


echo "Content-type: text/html; charset=utf-8"
echo ""

VLAN_DATA="$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge configurar mostrar bridge)"

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Configuració Tag-Untag Interface</title>
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
            <h2 class="card-title">Configuració d'Interfícies (Tag/Untag)</h2>
        </div>
        <div class="card-body">

<table>
<tr><th>Interfaç</th><th>UNTAG (PVID)</th><th>TAG (VIDs)</th><th style="width: 150px;">Accions</th></tr>
EOF

for iface in $(Interfaces_Ethernet); do
	# Check interface status
	STATUS_COLOR="var(--text-secondary)"
    STATUS_BG="#eee"
	STATUS_TEXT="UNKNOWN"
    
    # Simple check for UP/DOWN
	if ip link show "$iface" | grep -q "state UP"; then
		STATUS_COLOR="var(--success-color)"
        STATUS_BG="#e6f4ea"
		STATUS_TEXT="ACTIVA"
    else
        STATUS_COLOR="var(--danger-color)"
        STATUS_BG="#fce8e6"
        STATUS_TEXT="INACTIVA"
	fi

	echo "<tr>"
    echo "<td>"
    echo "<div style='font-weight: 500;'>$iface</div>"
    echo "<span style='font-size: 11px; padding: 2px 6px; border-radius: 10px; background: $STATUS_BG; color: $STATUS_COLOR;'>$STATUS_TEXT</span>"
    echo "</td>"
    
	linia_int=$(echo "$VLAN_DATA" | grep -E "^${iface};")
	VLAN_UNTAG=$(echo "$linia_int"|cut -d';' -f2)
	
    if [[ -z "$VLAN_UNTAG" ]]; then
	    echo "<td>-</td>"
	else
	    echo "<td>$VLAN_UNTAG</td>"
	fi
	
    VLAN_TAG=$(echo "$linia_int"|cut -d';' -f3)
	if [[ -z "$VLAN_TAG" ]]; then
	    echo "<td>-</td>"
	else
	    echo "<td>$VLAN_TAG</td>"
	fi
	
    echo "<td><a href='/cgi-bin/bridge-modificar-taguntag.cgi?int=$iface' class='btn secondary' style='padding: 4px 10px; font-size: 12px;'>Modificar</a></td>"
    echo "</tr>"
done

cat << EOF
</table>

<div style="margin-top: 24px; text-align: right;">
    <a href="/cgi-bin/bridge.cgi" class="btn secondary">Tornar al Bridge</a>
</div>

        </div>
    </div>
</div>
</body>
</html>
EOF
