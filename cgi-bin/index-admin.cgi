#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-Type:text/html;charset=utf-8"
/bin/cat << EOM

<html>
<head>
<title>Administrant el Router</title>
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
<body link="#E9AB17" vlink="#E9AB17" alink="#E9AB17">


EOM

echo "<h1 align="center">Administrant el Router "$HOSTNAME" amb "$PROJECTE"</h1>"

/bin/cat << EOM

<script>
function wan(){
window.top.frames['menu'].location.href='/cgi-bin/ifwan-menu.cgi';
window.top.frames['body'].location.href='/cgi-bin/ifwan.cgi?comand=estat&';
}
function enrutar(){
window.top.frames['menu'].location.href='/cgi-bin/enrutar-menu.cgi';
window.top.frames['body'].location.href='/cgi-bin/enrutar.cgi?comand=estat&';
}
function bridge(){
window.top.frames['menu'].location.href='/cgi-bin/bridge-menu.cgi';
window.top.frames['body'].location.href='/cgi-bin/bridge.cgi?comand=estat&';
}
function tallafocs(){
window.top.frames['menu'].location.href='/cgi-bin/tallafocs-menu.cgi';
window.top.frames['body'].location.href='/cgi-bin/tallafocs.cgi?comand=estat&';
}
</script>

<table width="100%">
  <tr>
    <td>
      <!-- Botons esquerra -->
      <button onclick="wan()">WAN</button>
      <button onclick="enrutar()">ENRUTAR</button> 
      <button onclick="bridge()">BRIDGE</button>    
      <button onclick="tallafocs()">TALLAFOCS</button>    
  </tr>
</table>

</body>
</html>

EOM


