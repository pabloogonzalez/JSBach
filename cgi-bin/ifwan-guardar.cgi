#!/bin/bash

# Load configuration
source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

# Extract parameters
mode=$(echo "$QUERY_STRING" | sed -n 's/^.*mode=\([^&]*\).*$/\1/p')
int=$(echo "$QUERY_STRING" | sed -n 's/^.*int=\([^&]*\).*$/\1/p')

# -- ERROR LAYOUT FUNCTION --
print_error() {
    cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error Configuració</title>
    <link rel="stylesheet" href="/style.css">
</head>
<body>
<div class="container" style="margin-top: 50px; max-width: 600px;">
    <div class="card" style="border-left: 5px solid var(--danger-color);">
        <div class="card-body">
            <h2 style="color: var(--danger-color);">$1</h2>
            <p>$2</p>
            <div style="margin-top: 20px;">
                <a href="/cgi-bin/ifwan-configurar.cgi" class="btn">Tornar</a>
            </div>
        </div>
    </div>
</div>
</body>
</html>
EOF
    exit 0
}

# Validation
if [ "$mode" == "manual" ]; then
	ip=$(echo "$QUERY_STRING" | sed -n 's/^.*ip=\([^&]*\).*$/\1/p')
	masc=$(echo "$QUERY_STRING" | sed -n 's/^.*masc=\([^&]*\).*$/\1/p')
	
	if [ -z "$ip" ] || [ -z "$masc" ]; then
		print_error "Camps obligatoris buits" "En mode manual, la IP i la Màscara són obligatòries."
	fi
	
	# Basic format validation
	if ! [[ "$ip" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
		print_error "Format IP invàlid" "La IP introduïda no té un format vàlid (x.x.x.x)."
	fi
    
    pe=$(echo "$QUERY_STRING" | sed -n 's/^.*pe=\([^&]*\).*$/\1/p')
	dns=$(echo "$QUERY_STRING" | sed -n 's/^.*dns=\([^&]*\).*$/\1/p')
fi


if [[ ! -z $ip ]]; then
	ipmas=$ip/$masc
fi

ordre="ifwan configurar $mode $int $ipmas $pe $dns"

# Execute command
RESULT=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli $ordre)

# Success Output
cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guardant Configuració</title>
    <link rel="stylesheet" href="/style.css">
    <!-- Redirect after 3 seconds -->
    <meta http-equiv="refresh" content="3;url=/cgi-bin/ifwan.cgi">
</head>
<body>

<nav class="navbar">
    <a href="/cgi-bin/main.cgi" class="navbar-brand">
        <span>📶</span> Router Admin
    </a>
    <div class="nav-links">
        <a href="/cgi-bin/ifwan.cgi" class="nav-link active">WAN</a>
        <a href="/cgi-bin/enrutar.cgi" class="nav-link">Enrutament</a>
        <a href="/cgi-bin/bridge.cgi" class="nav-link">Bridge</a>
        <a href="/cgi-bin/tallafocs.cgi" class="nav-link">Tallafocs</a>
    </div>
</nav>

<div class="container">
    <div class="card">
        <div class="card-header">
            <h2 class="card-title">Configuració Guardada</h2>
        </div>
        <div class="card-body">
            <div style="background: #e6f4ea; padding: 15px; border-radius: 4px; color: var(--success-color); border: 1px solid #ceead6;">
                <strong>Èxit:</strong> La configuració s'ha aplicat correctament.
            </div>
            
            <div style="margin-top: 20px;">
                <strong>Ordre executada:</strong><br>
                <code style="background: #eee; padding: 5px; border-radius: 4px; display: block; margin-top: 5px;">$ordre</code>
            </div>

             <div style="margin-top: 20px;">
                <strong>Resultat:</strong><br>
                <pre style="background: #f8f9fa; padding: 10px; border: 1px solid #ddd; border-radius: 4px;">$RESULT</pre>
            </div>
            
            <p style="margin-top: 20px; color: #666;">Redirigint a l'estat de la WAN en 3 segons...</p>
            <a href="/cgi-bin/ifwan.cgi" class="btn">Continuar ara</a>
        </div>
    </div>
</div>
</body>
</html>
EOF
