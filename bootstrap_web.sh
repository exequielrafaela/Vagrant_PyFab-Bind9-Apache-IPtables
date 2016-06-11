#ª/user/bin/env bash
apt-get update
apt-get install -y apache2
if ! [ -L /var/www ]; then
  rm -rf /var/www
  ln -fs /vagrant /var/www
fi

apt-get install inetutils-traceroute traceroute lynx

#ª/user/bin/env bash

echo "##########################"
echo "### STARTING NET CONF ####"
echo "##########################"
sudo service networking stop
sudo service networking start
sudo ip link set eth1 up
sudo ip addr add 172.16.0.1/24 dev eth1
sudo echo 1 >> /proc/sys/net/ipv4/ip_forward
sudo service ufw stop
sudo service apparmor teardown
#sudo ip route add 192.168.1.0/30 via 192.168.0.2
#sudo ip route add 192.168.2.0/30 via 192.168.0.2
#sudo ip route add 172.16.0.0/24 via 192.168.0.2
sudo ip route add default via 172.16.0.254 dev eth1
sudo echo nameserver 192.168.1.1 >> /etc/resolv.conf
sudo ip route del default via 10.0.2.2 dev eth0

echo "##########################"
echo "## NETWORK CONFIGURATION #"
echo "##########################"
netconf=$(ip addr show)
echo $netconf