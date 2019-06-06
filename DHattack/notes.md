# Get local ip address
ipconfig getifaddr en0
# Get external ip address
curl ifconfig.me
# Wireshark
filter statement: `(ip.dst==192.168.1.8)||(ip.src==192.168.1.8)`