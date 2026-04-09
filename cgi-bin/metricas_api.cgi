#!/bin/bash
# Deshabilitar comprobaciones globales no deseadas en modo CGI JSON
echo -e "Content-type: application/json\n"

# 1. Calcular uso de CPU basado en /proc/stat
# Se leen los "ticks" actuales, esperamos 0.1s y leemos de nuevo
read cpu a b c previdle rest < /proc/stat
prevtotal=$((a+b+c+previdle))
sleep 0.1
read cpu a b c idle rest < /proc/stat
total=$((a+b+c+idle))
# Calcula porcentaje de CPU
cpu_us=$(( 100 * ( (total-prevtotal) - (idle-previdle) ) / (total-prevtotal) ))

# 2. RAM (usando el comando local free)
# Expresado en Porcentaje, Usado GB, Total GB
ram_percent=$(free -m | awk 'NR==2{printf "%d", $3*100/$2}')
ram_used=$(free -m | awk 'NR==2{printf "%.1f", $3/1024}')
ram_total=$(free -m | awk 'NR==2{printf "%.1f", $2/1024}')

# 3. Disco (espacio libre en /)
disk_percent=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')

# 4. Uptime del Sistema
uptime_str=$(uptime -p | sed 's/up //')

# 5. Interfaz de Red Original (WAN)
source /usr/local/JSBach/conf/variables.conf
source /usr/local/JSBach/conf/$IFWAN_CONF
iface=${IFW_IFWAN:-enp1s0}

if [[ -e "/sys/class/net/$iface/statistics/rx_bytes" ]]; then
    rx=$(cat /sys/class/net/$iface/statistics/rx_bytes)
    tx=$(cat /sys/class/net/$iface/statistics/tx_bytes)
else
    rx=0
    tx=0
fi

# Devolver JSON Limpio
cat <<EOF
{
  "cpu": $cpu_us,
  "ram_percent": $ram_percent,
  "ram_text": "${ram_used} GB / ${ram_total} GB",
  "disk": $disk_percent,
  "uptime": "$uptime_str",
  "interface": "$iface",
  "rx_bytes": $rx,
  "tx_bytes": $tx
}
EOF
