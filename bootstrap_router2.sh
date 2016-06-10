#ª/user/bin/env bash

apt-get update
apt-get install inetutils-traceroute traceroute

echo "##########################"
echo "### STARTING NET CONF ####"
echo "##########################"
sudo service networking stop
sudo service networking start
sudo ip link set eth1 up
sudo ip addr add 192.168.1.2/30 dev eth1
sudo ip link set eth2 up
sudo ip addr add 192.168.2.1/30 dev eth2
sudo ip link set eth3 up
sudo ip addr add 172.16.2.254/30 dev eth3
sudo echo 1 >> /proc/sys/net/ipv4/ip_forward
sudo service ufw stop
sudo service apparmor teardown
sudo ip route add 172.16.1.0/24 via 192.168.1.1
sudo ip route add 192.168.0.0/24 via 192.168.1.1
sudo ip route add 172.16.0.0/24 via 192.168.2.2
sudo ip route add default via 192.168.1.1 dev eth1
sudo echo nameserver 192.168.1.1 >> /etc/resolv.conf
sudo ip route del default via 10.0.2.2 dev eth0

#apt-get update
#apt-get install inetutils-traceroute traceroute

echo "##########################"
echo "## NETWORK CONFIGURATION #"
echo "##########################"
netconf=$(ip addr show)
echo $netconf

