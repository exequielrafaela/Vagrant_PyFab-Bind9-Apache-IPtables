#ª/user/bin/env bash
apt-get update
sudo apt-get install bind9 dnsutils bind9utils bind9-doc
apt-get install inetutils-traceroute traceroute

echo "##########################"
echo "### STARTING NET CONF ####"
echo "##########################"
sudo service networking stop
sudo service networking start
sudo ip link set eth1 up
sudo ip addr add 10.0.0.1/30 dev eth1
sudo echo 1 >> /proc/sys/net/ipv4/ip_forward
sudo service ufw stop
sudo service apparmor teardown
sudo ip route add 20.0.0.0/30 via 10.0.0.2
sudo ip route add 30.0.0.0/30 via 10.0.0.2
sudo ip route add 172.16.0.0/24 via 10.0.0.2
sudo ip route add 192.168.1.0/24 via 10.0.0.2

echo "##########################"
echo "## NETWORK CONFIGURATION #"
echo "##########################"
netconf=$(ip addr show)
echo $netconf