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
    <title>Afegir Switch</title>
    <link rel="stylesheet" href="/style.css">
</head>
<body>

<nav class="navbar">
    <a href="/cgi-bin/main.cgi" class="navbar-brand">
        <span>📶</span> Router Admin
    </a>
    <div class="nav-links">
        <a href="/cgi-bin/switchs.cgi" class="nav-link">Tornar al llistat</a>
    </div>
</nav>

<div class="container">
    <div class="card" style="max-width: 600px; margin: 0 auto;">
        <div class="card-header">
            <h2 class="card-title">Afegir Nou Switch</h2>
        </div>
        <div class="card-body">
            <form action="/cgi-bin/switchs-configurar.cgi" method="get">
                <input type="hidden" name="accio" value="afegir">
                
                <div class="form-group" style="margin-bottom: 15px;">
                    <label for="nom" style="display:block; margin-bottom:5px; font-weight:500;">Nom del Switch:</label>
                    <input type="text" id="nom" name="nom" required style="width:100%; padding:8px; border:1px solid #ddd; border-radius:4px;">
                </div>

                <div class="form-group" style="margin-bottom: 15px;">
                    <label for="ip" style="display:block; margin-bottom:5px; font-weight:500;">Adreça IP:</label>
                    <input type="text" id="ip" name="ip" required pattern="^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$" placeholder="192.168.1.10" style="width:100%; padding:8px; border:1px solid #ddd; border-radius:4px;">
                </div>

                <div class="form-group" style="margin-bottom: 15px;">
                    <label for="user" style="display:block; margin-bottom:5px; font-weight:500;">Usuari d'Administració (SSH):</label>
                    <input type="text" id="user" name="user" required style="width:100%; padding:8px; border:1px solid #ddd; border-radius:4px;">
                </div>

                <div class="form-group" style="margin-bottom: 20px;">
                    <label for="pass" style="display:block; margin-bottom:5px; font-weight:500;">Contrasenya:</label>
                    <input type="password" id="pass" name="pass" required style="width:100%; padding:8px; border:1px solid #ddd; border-radius:4px;">
                </div>

                <div style="display: flex; gap: 10px;">
                    <button type="submit" class="btn">Afegir Switch</button>
                    <a href="/cgi-bin/switchs.cgi" class="btn secondary">Cancel·lar</a>
                </div>
            </form>
        </div>
    </div>
</div>

</body>
</html>
EOF
