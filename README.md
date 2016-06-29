# Vagrant_LinuxLab3

*_Vagrant and bash files for the Linux Networking 3rd Semester -  FINAL WORKSHOP_*
*PRACTICO INTEGRADOR (Será resuelto con Vagrant + VirtualBox + Bash)*

El objetivo del practico es instalar un Routers, Firewall y servicios adicionales (DNS/WebServer).

![alt tag](https://github.com/exequielrafaela/Vagrant_LinuxLab3/blob/master/images/Architecture Diagram.png)

*Instalar un servidor Web en un cliente en la red A escuchando en el puerto 8080.
*Otro cliente en la Red B debe ingresar al sitio www.practico-integrador.com y ser redirigido al host con el servidor Web en la Red A.

Para ello debe utilizar:
* DNS Bind9 (crear zona y mapas del dominio www.practico-integrador.com)
Vamos a tener que usar DNAT – Es decir cuando pongamos una URL y el DNS lo resuelva de todas formas lo forcemos a una dirección  IP de dest con DNAT.
* Ruteo
* IPTables (DNAT) / UFW
* Apache (instalacion por default escucha en puerto 80)

Pasos sugeridos a seguir:
* Configurar los Routers
* Instalar el servidor Web Apache en el cliente A y verificar que funcione locamente
* Crear las zonas y configurar el servicio dns en el Router 0.
* Configurar el Router con las IP Addresses necesarias.
* Verificar conectividad entre los router, y routers con los clientes.
* Verificar el acceso desde el router al servidor web.
* Verificar el acceso desde el cliente en la red B al servidor web (deberia resolverse por ruteo).
* Aplicar reglas de firewall para restringir el acceso via ssh solo desde las IPs de ambos host y realizar NAT y redireccion a la ip real del servidor web.

____________________________________________________________
____________________________________________________________

