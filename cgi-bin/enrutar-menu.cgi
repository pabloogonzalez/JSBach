#!/bin/bash


source /usr/local/JSBach/conf/variables.conf

/bin/cat << EOM

<html>
<head>
<meta http-equiv=Content-Type content="text/html; charset=windows-1252">
<meta content="MSHTML 6.00.2900.3660" name=GENERATOR> 

<style>
body { font-family: sans-serif; margin: 20px; background: #f6f6f6; }
h2 { background: #ddd; padding: 6px; }
table { border-collapse: collapse; margin-bottom: 20px; width: 80%; }
td, th { border: 1px solid #999; padding: 6px 10px; text-align: left; }
th { background: #f0f0f0; }
button { padding: 4px 10px; margin-left: 5px; }
</style>
</head>
<body>
<h4><a href="/cgi-bin/enrutar.cgi?comand=iniciar&" target="body">enrutar iniciar</a></h4>
<h4><a href="/cgi-bin/enrutar.cgi?comand=aturar&" target="body">enrutar aturar</a></h4>
<h4><a href="/cgi-bin/enrutar.cgi?comand=estat&" target="body">enrutar estat</a></h4>
</body>
</html>

EOM


