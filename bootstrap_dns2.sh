#ª/user/bin/env bash
sudo apt-get -y update
sudo apt-get -y install bind9 bind9utils bind9-doc
sudo apt-get -y install inetutils-traceroute traceroute vim

echo "##########################"
echo "### STARTING NET CONF ####"
echo "##########################"
sudo service networking stop
sudo service networking start
sudo ip link set eth1 up
sudo ip addr add 172.16.2.1/24 dev eth1
sudo echo 1 >> /proc/sys/net/ipv4/ip_forward
sudo service ufw stop
sudo service apparmor teardown
sudo ip route add default via 172.16.2.254 dev eth1
sudo echo nameserver 192.168.1.1 >> /etc/resolv.conf
sudo ip route del default via 10.0.2.2 dev eth0
sudo ip route del default via 10.0.2.2 dev eth0 metric 100

#vagrant@dns2:~$ ip route 
#default via 172.16.2.254 dev eth1 
#10.0.2.0/24 dev eth0  proto kernel  scope link  src 10.0.2.15 
#172.16.2.0/24 dev eth1  proto kernel  scope link  src 172.16.2.1 

echo "##########################"
echo "###### 1ry DNS CONF ######"
echo "##########################"
sudo cp /vagrant/NS2/hosts /etc/hosts
sudo cp /vagrant/NS2/bind9 /etc/default/bind9
sudo cp /vagrant/NS2/bind/named.conf.local /etc/bind/
sudo cp /vagrant/NS2/bind/named.conf.options /etc/bind/
sudo mkdir /etc/bind/zones
sudo cp /vagrant/NS2/bind/zones/db.practico-integrador.com /etc/bind/zones
sudo cp /vagrant/NS2/bind/zones/db.3.168.192  /etc/bind/zones
sudo cp /vagrant/NS2/bind/zones/db.1.168.192  /etc/bind/zones
sudo cp /vagrant/NS2/bind/zones/db.2.16.172  /etc/bind/zones
sudo service bind9 restart


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
#iptables -P OUTPUT ACCEPT
#iptables -P FORWARD DROP
#iptables -t nat -P PREROUTING ACCEPT
#iptables -t nat -P POSTROUTING ACCEPT

#iptables -I INPUT -i lo -j ACCEPT
#iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
#iptables -A OUTPUT -m state --state NEW,ESTABLISHED -j ACCEPT

## Reglas personalizadas
#iptables -t nat -A PREROUTING -i eth2 -d 172.168.2.1 -p tcp --dport 80 -j DNAT --to-destination 172.16.0.1:8080
##iptables -t nat -A PREROUTING -i eth2 -d 192.168.1.1 -p tcp --dport 80 -j DNAT --to-destination 172.16.0.1:8080

#iptables -A INPUT -j DROP

##To stop Ipv4 based iptables firewall
#sudo iptables-save > $HOME/firewall.txt
#sudo iptables -X
#sudo iptables -t nat -F
#sudo iptables -t nat -X
#sudo iptables -t mangle -F
#sudo iptables -t mangle -X
#sudo iptables -P INPUT ACCEPT
#sudo iptables -P FORWARD ACCEPT
#sudo iptables -P OUTPUT ACCEPT

#To stop Ipv6 based iptables firewall, enter:
#sudo ip6tables-save > $HOME/firewall-6.txt
#sudo ip6tables -X
#sudo ip6tables -t mangle -F
#sudo ip6tables -t mangle -X
#sudo ip6tables -P INPUT ACCEPT
#sudo ip6tables -P FORWARD ACCEPT
#sudo ip6tables -P OUTPUT ACCEPT

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