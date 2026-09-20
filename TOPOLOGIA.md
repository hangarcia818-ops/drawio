# Alcance de la topología

Laboratorio educativo PNETLab de monitoreo multisede.

| Sede | Routers | Switch capa 2 |
| --- | --- | --- |
| Bogotá | BOG_R1 y BACKUP_BOG | SW_BOG |
| Cali | CALI_R2 | SW_CALI |
| Medellín | MED_R4 | SW_MED |

Se emplean VLAN 10 ADMIN, VLAN 20 SOPORTE y VLAN 30 VENTAS.
La gestión utiliza VLAN 10; VLAN 99 fue eliminada.
El enrutamiento entre VLAN se realiza en subinterfaces de routers.

| Enlace | Red |
| --- | --- |
| Bogotá–Cali | 10.10.10.0/30 |
| Bogotá–Medellín | 10.10.10.4/30 |
| Cali–Medellín | 10.10.10.8/30 |
| Bogotá–respaldo | 10.10.10.24/30 |

OSPF utiliza el área 0. Bogotá cuenta con HSRP para las puertas de enlace
192.168.6.1, 192.168.4.1 y 192.168.0.1.
El respaldo comparte SW_BOG y no dispone de una WAN independiente del principal;
esta topología no proporciona redundancia completa ante cualquier fallo.

El servidor Ubuntu utiliza ens37 con 192.168.6.10/25 para el laboratorio y
ens33 mediante DHCP/NAT para Internet. La ruta predeterminada a Internet
corresponde a ens33; las redes remotas del laboratorio necesitan rutas por
192.168.6.1. El diagrama no instala ni valida estas rutas.

Servicios documentados: Nagios, Prometheus, Grafana, Node Exporter,
SNMP Exporter y GLPI. Su presencia no confirma que todos los dispositivos
estén siendo consultados correctamente.

Pendientes de confirmación: IP de gestión de SW_BOG, concesiones DHCP de
clientes, conectividad efectiva, reglas ACL y estado actual de monitoreo.

Los bloques VLAN agrupan usuarios y redes: no representan switches adicionales.
La conexión servidor–switch es lógica y omite el puente o nube de PNETLab.
Las consultas de monitoreo recorren la red existente; no son cables adicionales.
