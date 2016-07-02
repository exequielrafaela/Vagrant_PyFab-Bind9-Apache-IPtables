from fabric.api import run, sudo, settings, hide 
from termcolor import colored

def fw_nat_dns():
	with settings(warn_only=True):
		print colored('##########################', 'blue')
		print colored('####### FW_NAT_DNS #######', 'blue')
		print colored('##########################', 'blue')

		sudo('apt-get -y update')
		sudo('apt-get -y install bind9 bind9utils bind9-doc dnstop')
		sudo('apt-get -y install inetutils-traceroute traceroute tcpdump nmap vim')

		print colored('##########################', 'blue')
		print colored('### STARTING NET CONF ####', 'blue')
		print colored('##########################', 'blue')
		sudo('ip link set eth1 up')
		sudo('ip addr add 192.168.3.2/30 dev eth1')
		sudo('ip link set eth2 up')
		sudo('ip addr add 192.168.1.1/30 dev eth2')
		sudo('ip link set eth3 up')
		sudo('ip addr add 192.168.0.254/24 dev eth3')
		sudo('echo 1 >> /proc/sys/net/ipv4/ip_forward')
		sudo('service ufw stop')
		sudo('service apparmor teardown')
		sudo('service networking restart')

		print colored('##########################', 'blue')
		print colored('##### STATIC ROUTING #####', 'blue')
		print colored('##########################', 'blue')
		sudo('ip route add 172.16.0.0/24 via 192.168.1.2')
		sudo('ip route add 172.16.1.0/24 via 192.168.3.1')
		sudo('ip route add 172.16.2.0/24 via 192.168.1.2')
		sudo('ip route add default via 192.168.0.1 dev eth3')

		sudo('echo nameserver 192.168.0.1 >> /etc/resolv.conf')
		sudo('ip route del default via 10.0.2.2 dev eth0')

		print colored('##########################', 'blue')
		print colored('###### 1ry DNS CONF ######', 'blue')
		print colored('##########################', 'blue')
		sudo('cp /vagrant/conf/NS1/hosts /etc/hosts')	
		sudo('cp /vagrant/conf/NS1/bind9 /etc/default/bind9')
		sudo('cp /vagrant/conf/NS1/bind/named.conf.local /etc/bind/')
		sudo('cp /vagrant/conf/NS1/bind/named.conf.options /etc/bind/')
		sudo('mkdir /etc/bind/zones')
		sudo('cp /vagrant/conf/NS1/bind/zones/db.practico-integrador.com /etc/bind/zones')
		sudo('cp /vagrant/conf/NS1/bind/zones/db.3.168.192  /etc/bind/zones')
		sudo('cp /vagrant/conf/NS1/bind/zones/db.1.168.192  /etc/bind/zones')
		sudo('cp /vagrant/conf/NS1/bind/zones/db.2.16.172  /etc/bind/zones')
		sudo('service bind9 restart')


		print colored('##########################', 'blue')
		print colored('##### START FIREWALL #####', 'blue')
		print colored('##########################', 'blue')

		#To stop Ipv4 based iptables firewall
		sudo('iptables-save > $HOME/firewall.txt')
		sudo('iptables -X')
		sudo('iptables -t nat -F')
		sudo('iptables -t nat -X')
		sudo('iptables -t mangle -F')
		sudo('iptables -t mangle -X')
		sudo('iptables -P INPUT ACCEPT')
		sudo('iptables -P FORWARD ACCEPT')
		sudo('iptables -P OUTPUT ACCEPT')

		#To stop Ipv6 based iptables firewall, enter:
		sudo('ip6tables-save > $HOME/firewall-6.txt')
		sudo('ip6tables -X')
		sudo('ip6tables -t mangle -F')
		sudo('ip6tables -t mangle -X')
		sudo('ip6tables -P INPUT ACCEPT')
		sudo('ip6tables -P FORWARD ACCEPT')
		sudo('ip6tables -P OUTPUT ACCEPT')
		
		#To start Ipv4 based iptables firewall, enter:
		sudo('iptables -t nat -A PREROUTING -i eth2 -d 192.168.1.1 -p tcp --dport 80 -j DNAT --to-destination 172.16.0.1:8080')
		sudo('iptables -t nat -A PREROUTING -i eth1 -d 192.168.3.2 -p tcp --dport 80 -j DNAT --to-destination 172.16.0.1:8080')
		sudo('iptables -t nat -A PREROUTING -i eth1 -d 172.16.2.1 -p tcp --dport 80 -j DNAT --to-destination 172.16.0.1:8080')
		sudo('iptables -A INPUT -p tcp -s 10.0.2.2 --dport ssh -j ACCEPT')
		sudo('iptables -A INPUT -p tcp -s 172.16.0.1 --dport ssh -j ACCEPT')
		sudo('iptables -A INPUT -p tcp -s 172.16.1.1 --dport ssh -j ACCEPT')
		sudo('iptables -A INPUT -p tcp -s 172.16.2.1 --dport ssh -j ACCEPT')
		sudo('iptables -A INPUT -p tcp -s 0.0.0.0/0 --dport ssh -j DROP')

		print colored('######################################', 'blue')
		print colored('END FIREWALL - NAT TABLE STATUS:      ', 'blue')
		print colored('######################################', 'blue')
		with hide ('output'):
			fw=sudo('iptables -t nat -L')
		print colored (fw, 'red')

		print colored('######################################', 'blue')
		print colored('END FIREWALL - FILTER TABLE STATUS:   ', 'blue')
		print colored('######################################', 'blue')
		with hide ('output'):
			fw=sudo('iptables -L')
		print colored (fw, 'red')

		print colored('##########################', 'blue')
		print colored('## NETWORK CONFIGURATION #', 'blue')
		print colored('##########################', 'blue')
		with hide ('output'):
			netconf=sudo('ip addr show')
		print colored (netconf, 'yellow')

#############################################################################
#############################################################################

def dns2():
	with settings(warn_only=True):
		print colored('##########################', 'blue')
		print colored('########## DNS2 ##########', 'blue')
		print colored('##########################', 'blue')

		sudo('apt-get -y update')
		sudo('apt-get -y install bind9 bind9utils bind9-doc dnstop')
		sudo('apt-get -y install inetutils-traceroute traceroute tcpdump nmap vim')

		print colored('##########################', 'blue')
		print colored('### STARTING NET CONF ####', 'blue')
		print colored('##########################', 'blue')
		sudo('ip link set eth1 up')
		sudo('ip addr add 172.16.2.1/24 dev eth1')
		sudo('echo 1 >> /proc/sys/net/ipv4/ip_forward')
		sudo('service ufw stop')
		sudo('service apparmor teardown')
		
		print colored('##########################', 'blue')
		print colored('##### STATIC ROUTING #####', 'blue')
		print colored('##########################', 'blue')
		sudo('ip route add default via 172.16.2.254 dev eth1')
		sudo('echo nameserver 192.168.1.1 >> /etc/resolv.conf')
		sudo('ip route del default via 10.0.2.2 dev eth0')
		sudo('service networking restart')

		print colored('##########################', 'blue')
		print colored('###### 2ry DNS CONF ######', 'blue')
		print colored('##########################', 'blue')
		sudo('cp /vagrant/conf/NS2/hosts /etc/hosts')	
		sudo('cp /vagrant/conf/NS2/bind9 /etc/default/bind9')
		sudo('cp /vagrant/conf/NS2/bind/named.conf.local /etc/bind/')
		sudo('cp /vagrant/conf/NS2/bind/named.conf.options /etc/bind/')
		sudo('mkdir /etc/bind/zones')
		sudo('cp /vagrant/conf/NS2/bind/zones/db.practico-integrador.com /etc/bind/zones')
		sudo('cp /vagrant/conf/NS2/bind/zones/db.3.168.192  /etc/bind/zones')
		sudo('cp /vagrant/conf/NS2/bind/zones/db.1.168.192  /etc/bind/zones')
		sudo('cp /vagrant/conf/NS2/bind/zones/db.2.16.172  /etc/bind/zones')
		sudo('service bind9 restart')

		print colored('##########################', 'blue')
		print colored('##### START FIREWALL #####', 'blue')
		print colored('##########################', 'blue')

		#To stop Ipv4 based iptables firewall
		sudo('iptables-save > $HOME/firewall.txt')
		sudo('iptables -X')
		sudo('iptables -t nat -F')
		sudo('iptables -t nat -X')
		sudo('iptables -t mangle -F')
		sudo('iptables -t mangle -X')
		sudo('iptables -P INPUT ACCEPT')
		sudo('iptables -P FORWARD ACCEPT')
		sudo('iptables -P OUTPUT ACCEPT')

		#To stop Ipv6 based iptables firewall, enter:
		sudo('ip6tables-save > $HOME/firewall-6.txt')
		sudo('ip6tables -X')
		sudo('ip6tables -t mangle -F')
		sudo('ip6tables -t mangle -X')
		sudo('ip6tables -P INPUT ACCEPT')
		sudo('ip6tables -P FORWARD ACCEPT')
		sudo('ip6tables -P OUTPUT ACCEPT')
		
		#To start Ipv4 based iptables firewall, enter:
		sudo('iptables -t nat -A PREROUTING -i eth2 -d 192.168.1.1 -p tcp --dport 80 -j DNAT --to-destination 172.16.0.1:8080')
		sudo('iptables -t nat -A PREROUTING -i eth1 -d 192.168.3.2 -p tcp --dport 80 -j DNAT --to-destination 172.16.0.1:8080')
		sudo('iptables -t nat -A PREROUTING -i eth1 -d 172.16.2.1 -p tcp --dport 80 -j DNAT --to-destination 172.16.0.1:8080')
		sudo('iptables -A INPUT -p tcp -s 10.0.2.2 --dport ssh -j ACCEPT')
		sudo('iptables -A INPUT -p tcp -s 172.16.0.1 --dport ssh -j ACCEPT')
		sudo('iptables -A INPUT -p tcp -s 172.16.1.1 --dport ssh -j ACCEPT')
		sudo('iptables -A INPUT -p tcp -s 192.168.1.1 --dport ssh -j ACCEPT')
		sudo('iptables -A INPUT -p tcp -s 192.168.3.2 --dport ssh -j ACCEPT')
		sudo('iptables -A INPUT -p tcp -s 10.0.2.2 --dport ssh -j ACCEPT')
		sudo('iptables -A INPUT -p tcp -s 0.0.0.0/0 --dport ssh -j DROP')

		print colored('######################################', 'blue')
		print colored('END FIREWALL - NAT TABLE STATUS:      ', 'blue')
		print colored('######################################', 'blue')
		with hide ('output'):
			fw=sudo('iptables -t nat -L')
		print colored (fw, 'red')

		print colored('######################################', 'blue')
		print colored('END FIREWALL - FILTER TABLE STATUS:   ', 'blue')
		print colored('######################################', 'blue')
		with hide ('output'):
			fw=sudo('iptables -L')
		print colored (fw, 'red')

		print colored('##########################', 'blue')
		print colored('## NETWORK CONFIGURATION #', 'blue')
		print colored('##########################', 'blue')
		with hide ('output'):
			netconf=sudo('ip addr show')
		print colored (netconf, 'yellow')


#############################################################################
#############################################################################

def router1():
	with settings(warn_only=True):
		print colored('##########################', 'blue')
		print colored('######## ROUTER1 #########', 'blue')
		print colored('##########################', 'blue')

		sudo('apt-get -y update')
		sudo('apt-get -y install inetutils-traceroute traceroute tcpdump nmap vim')

		print colored('##########################', 'blue')
		print colored('### STARTING NET CONF ####', 'blue')
		print colored('##########################', 'blue')
		sudo('ip link set eth1 up')
		sudo('ip addr add 192.168.3.1/30 dev eth1')
		sudo('ip link set eth2 up')
		sudo('ip addr add 172.16.1.254/24 dev eth2')
		sudo('echo 1 >> /proc/sys/net/ipv4/ip_forward')
		sudo('service ufw stop')
		sudo('service apparmor teardown')
		
		print colored('##########################', 'blue')
		print colored('##### STATIC ROUTING #####', 'blue')
		print colored('##########################', 'blue')
		sudo('ip route add 192.168.1.0/30 via 192.168.3.2')
		sudo('ip route add 192.168.2.0/30 via 192.168.3.2')
		sudo('ip route add 172.16.0.0/24 via 192.168.3.2')
		sudo('ip route add 172.16.2.0/24 via 192.168.3.2')
		sudo('ip route add default via 192.168.3.2 dev eth1')
		sudo('echo nameserver 192.168.3.2 > /etc/resolv.conf')
		sudo('echo nameserver 172.16.2.1 >> /etc/resolv.conf')
		sudo('ip route del default via 10.0.2.2 dev eth0')
		sudo('service networking restart')

		print colored('##########################', 'blue')
		print colored('## NETWORK CONFIGURATION #', 'blue')
		print colored('##########################', 'blue')
		with hide ('output'):
			netconf=sudo('ip addr show')
		print colored (netconf, 'yellow')

#############################################################################
#############################################################################

def router2():
	with settings(warn_only=True):
		print colored('##########################', 'blue')
		print colored('######## ROUTER2 #########', 'blue')
		print colored('##########################', 'blue')

		sudo('apt-get -y update')
		sudo('apt-get -y install inetutils-traceroute traceroute tcpdump nmap vim')

		print colored('##########################', 'blue')
		print colored('### STARTING NET CONF ####', 'blue')
		print colored('##########################', 'blue')
		sudo('ip link set eth1 up')
		sudo('ip addr add 192.168.1.2/30 dev eth1')
		sudo('ip link set eth2 up')
		sudo('ip addr add 192.168.2.1/30 dev eth2')
		sudo('ip link set eth3 up')
		sudo('ip addr add 172.16.2.254/24 dev eth3')
		sudo('echo 1 >> /proc/sys/net/ipv4/ip_forward')
		sudo('service ufw stop')
		sudo('service apparmor teardown')
		
		print colored('##########################', 'blue')
		print colored('##### STATIC ROUTING #####', 'blue')
		print colored('##########################', 'blue')
		sudo('ip route add 172.16.1.0/24 via 192.168.1.1')
		sudo('ip route add 192.168.3.0/30 via 192.168.1.1')
		sudo('ip route add 172.16.0.0/24 via 192.168.2.2')
		sudo('ip route add default via 192.168.1.1 dev eth1')
		sudo('echo nameserver 192.168.1.1 > /etc/resolv.conf')
		sudo('echo nameserver 172.16.2.1 >> /etc/resolv.conf')
		sudo('ip route del default via 10.0.2.2 dev eth0')
		sudo('service networking restart')

		print colored('##########################', 'blue')
		print colored('## NETWORK CONFIGURATION #', 'blue')
		print colored('##########################', 'blue')
		with hide ('output'):
			netconf=sudo('ip addr show')
		print colored (netconf, 'yellow')

#############################################################################
#############################################################################

def router3():
	with settings(warn_only=True):
		print colored('##########################', 'blue')
		print colored('######## ROUTER3 #########', 'blue')
		print colored('##########################', 'blue')

		sudo('apt-get -y update')
		sudo('apt-get -y install inetutils-traceroute traceroute tcpdump nmap vim')

		print colored('##########################', 'blue')
		print colored('### STARTING NET CONF ####', 'blue')
		print colored('##########################', 'blue')
		sudo('ip link set eth1 up')
		sudo('ip addr add 192.168.2.2/30 dev eth1')
		sudo('ip link set eth2 up')
		sudo('ip addr add 172.16.0.254/24 dev eth2')
		sudo('echo 1 >> /proc/sys/net/ipv4/ip_forward')
		sudo('service ufw stop')
		sudo('service apparmor teardown')
		
		print colored('##########################', 'blue')
		print colored('##### STATIC ROUTING #####', 'blue')
		print colored('##########################', 'blue')
		sudo('ip route add 172.16.1.0/24 via 192.168.2.1')
		sudo('ip route add 172.16.2.0/24 via 192.168.2.1')
		sudo('ip route add 192.168.1.0/30 via 192.168.2.1')
		sudo('ip route add 192.168.0.0/24 via 192.168.2.1')
		sudo('ip route add default via 192.168.2.1 dev eth1')
		sudo('echo nameserver 192.168.1.1 > /etc/resolv.conf')
		sudo('echo nameserver 172.16.2.1 >> /etc/resolv.conf')
		sudo('ip route del default via 10.0.2.2 dev eth0')
		sudo('service networking restart')

		print colored('##########################', 'blue')
		print colored('## NETWORK CONFIGURATION #', 'blue')
		print colored('##########################', 'blue')
		with hide ('output'):
			netconf=sudo('ip addr show')
		print colored (netconf, 'yellow')

#############################################################################
#############################################################################

def web():
	with settings(warn_only=True):
		print colored('##########################', 'blue')
		print colored('######## WEB SERV ########', 'blue')
		print colored('##########################', 'blue')

		sudo('apt-get -y update')
		sudo('apt-get -y install inetutils-traceroute traceroute tcpdump nmap lynx-cur vim')
		sudo('apt-get -y install apache2')
		
		sudo('if ! [ -L /var/www ]; then'
  				'rm -rf /var/www'
  				'ln -fs /vagrant/ /var/www'
			'fi')
		
		print colored('##########################', 'blue')
		print colored('### STARTING NET CONF ####', 'blue')
		print colored('##########################', 'blue')
		sudo('ip link set eth1 up')
		sudo('ip addr add 172.16.0.1/24 dev eth1')
		sudo('echo 1 >> /proc/sys/net/ipv4/ip_forward')
		sudo('service ufw stop')
		sudo('service apparmor teardown')
		
		print colored('##########################', 'blue')
		print colored('##### STATIC ROUTING #####', 'blue')
		print colored('##########################', 'blue')
		sudo('ip route add default via 172.16.0.254 dev eth1')
		sudo('echo nameserver 192.168.1.1 > /etc/resolv.conf')
		sudo('echo nameserver 172.16.2.1 >> /etc/resolv.conf')
		sudo('ip route del default via 10.0.2.2 dev eth0')
		sudo('service networking restart')

		
		print colored('##########################', 'blue')
		print colored('#### APACHE2 WEB_SERV ####', 'blue')
		print colored('##########################', 'blue')
		sudo('wget -P /var/www/ -E -H -k -K -p http://www.binbash.com.ar')
		sudo('cp -r /var/www/www.binbash.com.ar/* /var/www/')
		sudo('echo "ServerName localhost" >> /etc/apache2/apache2.conf')
		sudo('cp /vagrant/Apache2/ports.conf /etc/apache2/ports.conf')
		sudo('sudo cp /vagrant/Apache2/default /etc/apache2/sites-available/default')
		sudo('service apache2 restart')
		sudo('service apache2 restart')

		print colored('##########################', 'blue')
		print colored('## NETWORK CONFIGURATION #', 'blue')
		print colored('##########################', 'blue')
		with hide ('output'):
			netconf=sudo('ip addr show')
		print colored (netconf, 'yellow')

#############################################################################
#############################################################################

def linux():
	with settings(warn_only=True):
		print colored('##########################', 'blue')
		print colored('######### LINUX ##########', 'blue')
		print colored('##########################', 'blue')

		sudo('apt-get -y update')
		sudo('apt-get -y install inetutils-traceroute traceroute tcpdump nmap vim lynx-cur')

		print colored('##########################', 'blue')
		print colored('### STARTING NET CONF ####', 'blue')
		print colored('##########################', 'blue')
		sudo('ip link set eth1 up')
		sudo('ip addr add 172.16.1.1/24 dev eth1')
		sudo('echo 1 >> /proc/sys/net/ipv4/ip_forward')
		sudo('service ufw stop')
		sudo('service apparmor teardown')
		
		print colored('##########################', 'blue')
		print colored('##### STATIC ROUTING #####', 'blue')
		print colored('##########################', 'blue')
		sudo('ip route add default via 172.16.1.254 dev eth1')
		sudo('echo nameserver 192.168.3.2 > /etc/resolv.conf')
		sudo('echo nameserver 172.16.2.1 >> /etc/resolv.conf')
		sudo('ip route del default via 10.0.2.2 dev eth0')
		sudo('service networking restart')

		print colored('##########################', 'blue')
		print colored('## NETWORK CONFIGURATION #', 'blue')
		print colored('##########################', 'blue')
		with hide ('output'):
			netconf=sudo('ip addr show')
		print colored (netconf, 'yellow')