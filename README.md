# ARP MitM Attack Script
**Autor:** Jonathan Sención  
**Matrícula:** 20250851  
**Institución:** ITLA - Instituto Tecnológico de las Américas  

---

## Objetivo del Laboratorio
Demostrar cómo un atacante puede realizar un ataque Man-in-the-Middle (MitM) mediante 
ARP Spoofing, envenenando las tablas ARP de los dispositivos víctima para interceptar 
todo el tráfico entre ellos.

---

## Objetivo del Script
Enviar respuestas ARP falsas tanto al target como al gateway, asociando la MAC del 
atacante con las IPs legítimas, logrando que todo el tráfico pase por Kali.

### Parámetros Usados
| Parámetro | Valor | Descripción |
|---|---|---|
| `target_ip` | `192.168.85.20` | IP de la víctima (VPC1) |
| `gateway_ip` | `192.168.85.1` | IP del gateway |
| `op=2` | ARP Reply | Tipo de paquete ARP |
| `iface` | `eth0` | Interfaz de red atacante |
| `interval` | `2s` | Intervalo entre envíos |

### Requisitos
- Kali Linux
- Python 3
- Scapy (`sudo apt install python3-scapy`)
- IP Forwarding habilitado (`sudo sysctl -w net.ipv4.ip_forward=1`)
- Ejecutar como root (`sudo`)

---

## Funcionamiento del Script
1. Se obtiene la MAC del target y del gateway con `getmacbyip()`
2. Se envían ARP Replies falsos al target diciéndole que el gateway es Kali
3. Se envían ARP Replies falsos al gateway diciéndole que el target es Kali
4. Todo el tráfico entre target y gateway fluye por Kali
5. Al detener el script, las tablas ARP se restauran automáticamente

---

## Topología de Red
[Kali Atacante] eth0 ──── e0/2 [SW1] e0/0 ──── e0/0 [SW2] e0/1 ──── eth0 [VPC1]
192.168.85.10                10.20.25.1              10.20.25.2         192.168.85.20
│
e0/1 └──── e0/0 [SW3] e0/1 ──── eth0 [VPC2]
10.20.25.3         192.168.51.20

### VLANs
| VLAN | Nombre | Red |
|---|---|---|
| VLAN 10 | VLAN10-20250851 | 192.168.85.0/24 |
| VLAN 20 | VLAN20-20250851 | 192.168.51.0/24 |
| Management | MGMT | 10.20.25.0/24 |

---

## Ejecución
```bash
sudo sysctl -w net.ipv4.ip_forward=1
sudo python3 arp_mitm.py
```

### Verificación del Ataque
En VPC1:
show arp
La MAC del gateway debe ser la MAC de Kali.

---

## Capturas de Pantalla
<img width="849" height="749" alt="image" src="https://github.com/user-attachments/assets/3bb19810-a94e-4344-b1e3-c29ec6b9d6c3" />

<img width="763" height="314" alt="image" src="https://github.com/user-attachments/assets/3690a9ad-a7db-488f-8bc8-9469040d0a9c" />

<img width="650" height="554" alt="image" src="https://github.com/user-attachments/assets/e31ef177-5daa-4c4a-9284-7842ac82f3e2" />

---

## Contramedidas
### 1. Dynamic ARP Inspection (DAI)
ip arp inspection vlan 10
interface e0/1
ip arp inspection limit rate 100
### 2. ARP estático en dispositivos críticos
arp 192.168.85.1 aabb.cc00.2000 arpa
### 3. DHCP Snooping (requerido para DAI)
ip dhcp snooping
ip dhcp snooping vlan 10
