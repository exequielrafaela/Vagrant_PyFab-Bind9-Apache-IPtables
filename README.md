# vagrant_UNC-3
Vagrant and bash files for the Linux Networking 3rd Semester -  FINAL WORKSHOP

PRACTICO INTEGRADOR (Será resuelto con Vagrant + VirtualBox + Bash)

El objetivo del practico es instalar un Router, un Firewall (pueden ser en la misma maquina) y servicios adicionales.

*Un Router con 2 interfaces de red (2 redes distintas A y B). Recordar que deberán ser 4 Routers:

_____________________________________________________________________________________________________
DIAGRAMA TOPOLÓGICO: 								                      
                        (R1/FW/DNAT(IPtables)/DNS)<=>(INTERNET GW 192.168.0.1/24)                    
		        10.0.0.1/30        			                                     
		         ||                                      		                     
   	      		10.0.0.2/30				 		 		             
(R4)<==================>(R2)<====================>(R3)<=>("NW_A": 172.16.0.0/24 - Apache:8080)       
20.0.0.1/30 20.0.0.2/30    30.0.0.1/30 30.0.0.2/30    172.16.0.254/24     172.16.0.1/24              
192.168.0.254/24                                                          www.practico-integrador.com                             
||					                                  
("NW_B":192.168.1.0/24 - Client)								                                192.168.1.1/24                                                                                      _____________________________________________________________________________________________________
  
*Instalar un servidor Web en un cliente en la red A escuchando en el puerto 8080.
*Otro cliente en la Red B debe ingresar al sitio www.practico-integrador.com y ser redirigido al host con el servidor Web en la Red A.

Para ello debe utilizar:
* DNS (crear zona y mapas del dominio www.practico-integrador.com)
Vamos a tener que usar DNAT – Es decir cuando pongamos una URL y el DNS lo resuelva de todas formas lo forcemos a una dirección  IP de dest con DNAT.
* Ruteo
* IPTables
* Apache (instalacion por default escucha en puerto 80)

Pasos sugeridos a seguir:
* Instalar el servidor Web Apache en el cliente A y verificar que funcione locamente
* Crear las zoas y configurar el servicio dns en el Router.
* Configurar el Router con las 2 ips.
* Verificar conectividad entre el router y los 2 clientes.
* Verificar el acceso desde el router al servidor web.
* Verificar el acceso desde el cliente en la red B al servidor web (deberia resolverse por ruteo).
* Aplicar reglas de firewall: 
* para restringir el acceso via ssh solo desde las ips de ambos host.

____________________________________________________________
____________________________________________________________

Ejercicios de Ruteo

El objetivo es armar una topologia con Router que interconecte como mínimo 2 redes. Elija las redes e interconecte los host (de distintas redes) a traves del router.

* Configure el router con las interfaces fisicas y/o virtuales que necesite
* Realize pruebas de conectividad con alguna herramienta
* Armar la tabla reducida de ruteo.

Tener en cuenta:
* ip forwarding esta activado
* selinux no bloquee conexiones
* iptables no bloquee conexiones
* Las interfaces esten bien configuradas

____________________________________________________________
____________________________________________________________

Tips Armar Router Linux

1) ip link set eth0 up
2) ip addr add 192.168.0.2/24 dev eth0 (ip addr del 192.168.0.2/24 dev eth0)
3) ip addr add 172.16.0.2/24 dev eth0
4) ip route add default via 192.168.0.1
5) cat /proc/sys/net/ipv4/ip_forward
Verificar si es 0 (desactivado) o 1 (activado)
sudo echo 1 >> /proc/sys/net/ipv4/ip_forward (On the Fly)
vi /etc/sysctl.conf => Descomentar net.ipv4.ip_forward=1 (De forma permanente)
6) sudo vi /etc/selinux/config => SELINUX=permissive
7) Deteber AppArmor & UFW
8)sudo /etc/init.d/iptables stop
Luego aplicar reglas necesarias
9)sudo ip route add 200.16.16.61/32 via 172.16.0.1
La ip de otro router por ejemplo
sudo ip route del 200.16.16.61
10)traceroute www.unc.edu.ar
Comprobar que trata de enviarlo via 172.16.0.1 y no la default GW 192.168.0.1

____________________________________________________________
____________________________________________________________

Clase9

Iproute2:
https://es.wikipedia.org/wiki/Iproute2

Iproute2 Commands:
http://www.mauriciomatamala.net/PAR/iproute2.php

Mostrar dispositivos de red y su configuración.
	ifconfig
	ip addr show // ip link show

Activar una interfaz de red.
	ifconfig eth0 up
	ip link set eth0 up

Desactivar una interfaz de red.
	ifconfig eth0 down
	ip link set eth0 down

Establecer una dirección IP a una interfaz.
	ifconfig eth0 192.168.1.1
	ip address add 192.168.1.1 dev eth0

Eliminar una dirección IP de una interfaz.
	ifconfig no podrá hacer esto.
	ip address del 192.168.1.1 dev eth0

Añadir una interfaz virtual.
	ifconfig eth0:1 10.0.0.1/8
	ip addr add 10.0.0.1/8 dev eth0 label eth0:1

Añadir una entrada en la tabla ARP.
	arp -i eth0 -s 192.168.0.1 00:11:22:33:44:55
	ip neigh add 192.168.0.1 lladdr 00:11:22:33:44:55 nud permanent dev eth0

Desconectar un dispositivo ARP.
	ifconfig -arp eth0
	ip link set dev eth0 arp off

Para configurar una tarjeta de red física, por ejemplo, con ifconfig debemos teclear lo siguiente:
	ifconfig eth0 192.168.0.2 netmask 255.255.255.0
	ip addr add 192.168.0.2/24 dev eth0

Ver opciones
	man ip

____________________________________________________________
____________________________________________________________
