#!/bin/bash


source /usr/local/JSBach/conf/variables.conf

/bin/cat << EOM

<html>
<head>
<meta http-equiv=Content-Type content="text/html; charset=windows-1252">
<meta content="MSHTML 6.00.2900.3660" name=GENERATOR> 

EOM
cat $DIR/$PROJECTE/$DIR_CGI/$CSS_CGI_BIN
/bin/cat << EOM

</head>
<body>
<h4><a href="/cgi-bin/dmz.cgi?comand=iniciar&" target="body">dmz iniciar</a></h4>
<h4><a href="/cgi-bin/dmz.cgi?comand=aturar&" target="body">dmz aturar</a></h4>
<h4><a href="/cgi-bin/dmz.cgi?comand=estat&" target="body">dmz estat</a></h4>
<h4><a href="/cgi-bin/dmz-configurar.cgi" target="body">dmz configuracio</a></h4>
</body>
</html>

EOM


