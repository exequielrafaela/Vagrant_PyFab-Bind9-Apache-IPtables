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
sudo ip addr add 10.0.0.2/30 dev eth1
sudo ip link set eth2 up
sudo ip addr add 192.168.0.2/30 dev eth2
sudo ip link set eth3 up
sudo ip addr add 192.168.1.1/30 dev eth3
sudo echo 1 >> /proc/sys/net/ipv4/ip_forward
sudo service ufw stop
sudo service apparmor teardown
sudo ip route add 192.168.1.0/30 via 192.168.1.2
sudo ip route add 172.16.0/24 via 192.168.1.2
sudo ip route add 172.16.1.0/24 via 192.168.0.1

echo "##########################"
echo "#### Inicio Firewall ####"
echo "##########################"

## FLUSH/Borrado de reglas
##FLush
#iptables -F
##Delete User Chains
#iptables -X
##Reset Counter
#iptables -Z
##Delete Chains Nat Table
#iptables -t nat -F

## Establecemos politica por defecto
#iptables -P INPUT DROP
#iptables -P INPUT ACCEPT
#iptables -P OUTPUT DROP
#iptables -P OUTPUT ACCEPT
#iptables -P FORWARD DROP
#iptables -P FORWARD ACCEPT
#iptables -t nat -P PREROUTING ACCEPT
#iptables -t nat -P POSTROUTING ACCEPT

#iptables -I INPUT -i lo -j ACCEPT
#iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
#iptables -A OUTPUT -m state --state NEW,ESTABLISHED -j ACCEPT

## Reglas personalizadas
#iptables -t nat -A PREROUTING -i eth2 -d 192.168.0.2 -p tcp --dport 80 -j DNAT --to-destination 172.16.0.1:8080
#iptables -t nat -A PREROUTING -i eth1 -d 192.168.1.1 -p tcp --dport 80 -j DNAT --to-destination 172.16.0.1:8080

#iptables -A INPUT -j DROP

#To stop Ipv4 based iptables firewall
sudo iptables-save > $HOME/firewall.txt
sudo iptables -X
sudo iptables -t nat -F
sudo iptables -t nat -X
sudo iptables -t mangle -F
sudo iptables -t mangle -X
sudo iptables -P INPUT ACCEPT
sudo iptables -P FORWARD ACCEPT
sudo iptables -P OUTPUT ACCEPT

#To stop Ipv6 based iptables firewall, enter:
sudo ip6tables-save > $HOME/firewall-6.txt
sudo ip6tables -X
sudo ip6tables -t mangle -F
sudo ip6tables -t mangle -X
sudo ip6tables -P INPUT ACCEPT
sudo ip6tables -P FORWARD ACCEPT
sudo ip6tables -P OUTPUT ACCEPT

echo "######################################"
echo "Fin Firewall . Verificar: iptables -nL"
echo "######################################"
fw=$(iptables -nL)
echo $fw

echo "##########################"
echo "## NETWORK CONFIGURATION #"
echo "##########################"
netconf=$(ip addr show)
echo $netconf