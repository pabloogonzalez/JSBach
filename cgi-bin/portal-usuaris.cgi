#!/bin/bash

# Load variables
source /usr/local/JSBach/conf/variables.conf
CONF_USUARIS="$DIR/$PROJECTE/$DIR_CONF/usuaris_wifi.conf"

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestió Portal Captiu</title>
    <link rel="stylesheet" href="/style.css">
    <style>
        .table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        .table th, .table td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        .table th { background-color: #f2f2f2; color: #333; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
        .form-group input { width: 100%; padding: 8px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }
    </style>
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
        <a href="/cgi-bin/portal-usuaris.cgi" class="nav-link active">Portal Captiu</a>
    </div>
</nav>

<div class="container">
    <div class="card">
        <div class="card-header">
            <h2 class="card-title">Gestió d'Usuaris (WiFi)</h2>
        </div>
        <div class="card-body">
            <p>Afegeix o elimina usuaris que tenen accés a la xarxa a través del portal captiu.</p>
            
            <h3>Afegir Nou Usuari</h3>
            <div style="background: #f9f9f9; padding: 20px; border: 1px solid #eee; border-radius: 8px; margin-bottom: 30px;">
                <form action="/cgi-bin/portal-usuaris-guardar.cgi" method="POST">
                    <div class="form-group">
                        <label for="new_user">Nom d'Usuari:</label>
                        <input type="text" id="new_user" name="usuario" required>
                    </div>
                    <div class="form-group">
                        <label for="new_pass">Contrasenya:</label>
                        <input type="password" id="new_pass" name="password" required>
                    </div>
                    <button type="submit" class="btn">Desar Usuari</button>
                </form>
            </div>

            <h3>Usuaris Registrats</h3>
            <table class="table">
                <thead>
                    <tr>
                        <th>Usuari</th>
                        <th>Contrasenya</th>
                        <th>Accions</th>
                    </tr>
                </thead>
                <tbody>
EOF

if [ -f "$CONF_USUARIS" ]; then
    # Leer el archivo línea a línea evitando problemas
    while IFS=';' read -r conf_user conf_pass; do
        conf_user=$(echo "$conf_user" | tr -d '\r')
        conf_pass=$(echo "$conf_pass" | tr -d '\r')
        
        # Ignorar lineas vacias
        if [ -n "$conf_user" ]; then
            echo "<tr>"
            echo "<td>$conf_user</td>"
            echo "<td>$conf_pass</td>"
            echo "<td><a href='/cgi-bin/portal-usuaris-eliminar.cgi?usuario=$conf_user' class='btn secondary' style='color: #d93025; border-color: #d93025; padding: 6px 12px;'>Eliminar</a></td>"
            echo "</tr>"
        fi
    done < "$CONF_USUARIS"
fi

cat << EOF
                </tbody>
            </table>
        </div>
    </div>
</div>

</body>
</html>
EOF
