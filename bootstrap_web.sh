#ª/user/bin/env bash
sudo apt-get -y update
sudp apt-get -y install inetutils-traceroute traceroute lynx-cur vim

sudo apt-get -y install apache2
if ! [ -L /var/www ]; then
  rm -rf /var/www
  ln -fs /vagrant/ /var/www
fi

sudp apt-get -y install inetutils-traceroute traceroute lynx

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
#sudo ip route add 192.168.1.0/30 via 192.168.3.2
#sudo ip route add 192.168.2.0/30 via 192.168.3.2
#sudo ip route add 172.16.0.0/24 via 192.168.3.2
sudo ip route add default via 172.16.0.254 dev eth1
sudo echo nameserver 192.168.1.1 > /etc/resolv.conf
sudo ip route del default via 10.0.2.2 dev eth0
sudo ip route del default via 10.0.2.2 dev eth0 metric 100

sudo cp /vagrant/Apache2/default /etc/apache2/sites-available/default
sudo service apache2 restart

echo "##########################"
echo "## NETWORK CONFIGURATION #"
echo "##########################"
netconf=$(ip addr show)
echo $netconf