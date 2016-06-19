#ª/user/bin/env bash
sudo apt-get -y update
sudo apt-get -y install inetutils-traceroute traceroute vim

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
sudo ip addr add 172.16.2.254/24 dev eth3
sudo echo 1 >> /proc/sys/net/ipv4/ip_forward
sudo service ufw stop
sudo service apparmor teardown
sudo ip route add 172.16.1.0/24 via 192.168.1.1
sudo ip route add 192.168.3.0/30 via 192.168.1.1
sudo ip route add 172.16.0.0/24 via 192.168.2.2
sudo ip route add default via 192.168.1.1 dev eth1
sudo echo nameserver 192.168.1.1 > /etc/resolv.conf
sudo ip route del default via 10.0.2.2 dev eth0
sudo ip route del default via 10.0.2.2 dev eth0 metric 100

#vagrant@router2:~$ ip route 
#default via 192.168.1.1 dev eth1 
#10.0.2.0/24 dev eth0  proto kernel  scope link  src 10.0.2.15 
#172.16.0.0/24 via 192.168.2.2 dev eth2 
#172.16.1.0/24 via 192.168.1.1 dev eth1 
#172.16.2.0/24 dev eth3  proto kernel  scope link  src 172.16.2.254 
#192.168.0.0/24 via 192.168.1.1 dev eth1 
#192.168.1.0/30 dev eth1  proto kernel  scope link  src 192.168.1.2 
#192.168.2.0/30 dev eth2  proto kernel  scope link  src 192.168.2.1 
#192.168.3.0/30 via 192.168.1.1 dev eth1 

echo "##########################"
echo "## NETWORK CONFIGURATION #"
echo "##########################"
netconf=$(ip addr show)
echo $netconf

