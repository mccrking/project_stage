import nmap
import socket
import subprocess
import platform
import re
from datetime import datetime
import time
import os
os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\Nmap"

# Fonction pour obtenir l'heure locale
def get_local_time():
    """Retourne l'heure locale actuelle"""
    return datetime.now()

class NetworkScanner:
    def __init__(self):
        self.nm = None
        self.nmap_available = False
        try:
            self.nm = nmap.PortScanner()
            self.nmap_available = True
        except Exception as e:
            print(f"⚠️ Nmap non disponible: {str(e)}")
            print("🔄 Le mode fallback sera utilisé pour les scans réseau")
        
        self.device_types = {
            'router': ['router', 'gateway', 'firewall'],
            'server': ['server', 'srv', 'dc', 'domain'],
            'printer': ['printer', 'print', 'hp', 'canon', 'epson'],
            'workstation': ['pc', 'workstation', 'desktop', 'laptop'],
            'switch': ['switch', 'sw', 'hub'],
            'camera': ['camera', 'cam', 'ipcam'],
            'phone': ['phone', 'voip', 'sip'],
            'automation': ['plc', 'automate', 'scada', 'hmi']
        }
    
    def discover_networks(self):
        """
        Découvre automatiquement tous les réseaux disponibles
        
        Returns:
            list: Liste des réseaux détectés avec leurs informations
        """
        networks = []
        
        try:
            # Utiliser socket pour obtenir l'adresse IP locale
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            # Détecter automatiquement les réseaux courants
            ip_parts = local_ip.split('.')
            
            # Réseaux basés sur l'IP locale
            detected_networks = [
                f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24",  # Réseau local
                f"{ip_parts[0]}.{ip_parts[1]}.0.0/16",              # Réseau étendu
            ]
            
            # Réseaux Central Danone (production)
            from config import Config
            production_networks = Config.PRODUCTION_NETWORKS
            
            # Ajouter des réseaux courants si pas déjà présents
            common_networks = [
                '192.168.0.0/24', 
                '192.168.100.0/24'
            ]
            
            # Combiner réseaux Central Danone et courants
            all_networks = list(set(production_networks + common_networks))
            
            # Combiner et dédupliquer
            all_networks = list(set(detected_networks + all_networks))
            
            for network in all_networks:
                network_info = {
                    'interface': 'auto-detected',
                    'ip': network.split('/')[0],
                    'netmask': '255.255.255.0',
                    'network_range': network,
                    'total_addresses': 256,
                    'detected_from': 'local_ip' if network in detected_networks else 'common'
                }
                
                networks.append(network_info)
                
        except Exception as e:
            print(f"⚠️ Erreur détection réseaux: {str(e)}")
            # Fallback: réseaux de base
            fallback_networks = [
                '192.168.1.0/24',
                '192.168.0.0/24'
            ]
            
            for network in fallback_networks:
                networks.append({
                    'interface': 'fallback',
                    'ip': network.split('/')[0],
                    'netmask': '255.255.255.0',
                    'network_range': network,
                    'total_addresses': 256,
                    'detected_from': 'fallback'
                })
        
        return networks
    
    def _calculate_network_range(self, ip, netmask):
        """
        Calcule la plage réseau à partir d'une IP et d'un masque
        
        Args:
            ip (str): Adresse IP
            netmask (str): Masque de sous-réseau
            
        Returns:
            str: Plage réseau au format CIDR
        """
        try:
            # Convertir IP et masque en entiers
            ip_parts = [int(x) for x in ip.split('.')]
            mask_parts = [int(x) for x in netmask.split('.')]
            
            # Calculer l'adresse réseau
            network_parts = []
            for i in range(4):
                network_parts.append(ip_parts[i] & mask_parts[i])
            
            network_ip = '.'.join(map(str, network_parts))
            
            # Calculer le CIDR
            cidr = sum(bin(int(x)).count('1') for x in mask_parts)
            
            return f"{network_ip}/{cidr}"
            
        except Exception as e:
            print(f"❌ Erreur calcul plage réseau: {str(e)}")
            return f"{ip}/24"
    
    def _calculate_total_addresses(self, netmask):
        """
        Calcule le nombre total d'adresses dans un réseau
        
        Args:
            netmask (str): Masque de sous-réseau
            
        Returns:
            int: Nombre total d'adresses
        """
        try:
            mask_parts = [int(x) for x in netmask.split('.')]
            cidr = sum(bin(int(x)).count('1') for x in mask_parts)
            return 2 ** (32 - cidr)
        except:
            return 256
    
    def scan_all_networks(self):
        """
        Scanne tous les réseaux détectés
        
        Returns:
            dict: Résultats du scan pour chaque réseau
        """
        networks = self.discover_networks()
        all_results = {}
        
        print(f"🔍 Découverte de {len(networks)} réseau(x)")
        
        for network_info in networks:
            network_range = network_info['network_range']
            print(f"📡 Scan du réseau: {network_range}")
            
            try:
                devices = self.scan_network(network_range)
                all_results[network_range] = {
                    'network_info': network_info,
                    'devices': devices,
                    'scan_time': get_local_time().isoformat()
                }
                
                print(f"✅ {network_range}: {len(devices)} équipements trouvés")
                
            except Exception as e:
                print(f"❌ Erreur scan {network_range}: {str(e)}")
                all_results[network_range] = {
                    'network_info': network_info,
                    'devices': [],
                    'error': str(e),
                    'scan_time': get_local_time().isoformat()
                }
        
        return all_results
    
    def scan_network(self, network_range):
        """
        Scanne le réseau pour détecter les appareils actifs
        
        Args:
            network_range (str): Plage réseau à scanner (ex: "192.168.1.0/24")
            
        Returns:
            list: Liste des appareils détectés avec leurs informations
        """
        print(f"🔍 Démarrage du scan réseau sur {network_range}")
        start_time = time.time()
        
        # Utiliser nmap si disponible, sinon fallback
        if self.nmap_available and self.nm:
            try:
                # Scan rapide avec nmap
                scan_result = self.nm.scan(
                    hosts=network_range,
                    arguments='-sn -n --max-retries 2 --host-timeout 10s'
                )
                
                devices = []
                
                for host in self.nm.all_hosts():
                    if self.nm[host].state() == 'up':
                        device_info = self._get_device_info(host)
                        if device_info:
                            devices.append(device_info)
                
                scan_duration = time.time() - start_time
                print(f"✅ Scan nmap terminé en {scan_duration:.2f}s - {len(devices)} appareils détectés")
                
                return devices
                
            except Exception as e:
                print(f"❌ Erreur lors du scan nmap: {str(e)}")
                print("🔄 Passage au mode fallback...")
        
        # Fallback: scan simple avec ping
        return self._fallback_scan(network_range)
    
    def _get_device_info(self, ip_address):
        """
        Récupère les informations détaillées d'un appareil
        
        Args:
            ip_address (str): Adresse IP de l'appareil
            
        Returns:
            dict: Informations de l'appareil
        """
        try:
            device_info = {
                'ip': ip_address,
                'mac': '',
                'hostname': '',
                'type': 'Unknown',
                'scan_time': get_local_time().isoformat(),
                'is_online': True  # Ajout pour compatibilité dashboard/base
            }
            
            # Récupérer le nom d'hôte
            try:
                hostname = socket.gethostbyaddr(ip_address)[0]
                device_info['hostname'] = hostname
            except:
                device_info['hostname'] = f"Unknown-{ip_address.split('.')[-1]}"
            
            # Récupérer l'adresse MAC (si disponible avec nmap)
            mac_vendor = ''
            if self.nmap_available and self.nm and ip_address in self.nm.all_hosts():
                try:
                    mac = self.nm[ip_address]['addresses'].get('mac', '')
                    device_info['mac'] = mac
                    # Vendor MAC (si disponible)
                    vendor_dict = self.nm[ip_address].get('vendor', {})
                    if isinstance(vendor_dict, dict) and vendor_dict:
                        mac_vendor = list(vendor_dict.values())[0]
                    elif isinstance(vendor_dict, str):
                        mac_vendor = vendor_dict
                    else:
                        mac_vendor = ''
                    device_info['mac_vendor'] = mac_vendor
                except Exception as e:
                    print(f"⚠️ Erreur extraction vendor MAC pour {ip_address}: {str(e)}")
                    device_info['mac_vendor'] = ''
            else:
                device_info['mac_vendor'] = ''
            # Déterminer le type d'appareil (hostname + vendor)
            device_info['type'] = self._detect_device_type(device_info['hostname'], device_info.get('mac_vendor', ''))
            
            return device_info
            
        except Exception as e:
            print(f"⚠️ Erreur lors de la récupération des infos pour {ip_address}: {str(e)}")
            return None
    
    def _detect_device_type(self, hostname, mac_vendor=None):
        """
        Détermine le type d'appareil basé sur le nom d'hôte et le vendor MAC
        Args:
            hostname (str): Nom d'hôte de l'appareil
            mac_vendor (str): Vendor MAC (optionnel)
        Returns:
            str: Type d'appareil détecté
        """
        hostname_lower = (hostname or '').lower()
        mac_vendor_lower = (mac_vendor or '').lower()

        # Règles enrichies sur le nom d'hôte
        keywords = {
            'router': ['router', 'gateway', 'firewall', 'zte', 'livebox', 'bbox', 'freebox', 'box', 'netgear', 'tplink', 'dlink', 'cisco'],
            'server': ['server', 'srv', 'dc', 'domain', 'nas', 'synology', 'qnap'],
            'printer': ['printer', 'print', 'hp', 'canon', 'epson', 'brother', 'xerox', 'ricoh'],
            'workstation': ['pc', 'workstation', 'desktop', 'laptop', 'win', 'macbook', 'imac', 'lenovo', 'dell', 'asus', 'acer', 'msi', 'hp'],
            'switch': ['switch', 'sw', 'hub', 'cisco', 'netgear', 'tplink'],
            'camera': ['camera', 'cam', 'ipcam', 'hikvision', 'dahua', 'foscam', 'arlo'],
            'phone': ['phone', 'voip', 'sip', 'iphone', 'android', 'samsung', 'huawei', 'xiaomi', 'oneplus', 'ipad', 'tablet'],
            'automation': ['plc', 'automate', 'scada', 'hmi', 'siemens', 'schneider', 'abb', 'mitsubishi']
        }
        # 1. Par hostname
        for device_type, kw_list in keywords.items():
            for kw in kw_list:
                if kw in hostname_lower:
                    return device_type.title()
        # 2. Par vendor MAC
        if mac_vendor_lower:
            if any(v in mac_vendor_lower for v in ['cisco', 'netgear', 'tplink', 'dlink']):
                return 'Switch'
            if any(v in mac_vendor_lower for v in ['hp', 'canon', 'epson', 'brother', 'xerox', 'ricoh']):
                return 'Printer'
            if any(v in mac_vendor_lower for v in ['apple', 'samsung', 'huawei', 'xiaomi', 'oneplus']):
                return 'Phone'
            if any(v in mac_vendor_lower for v in ['siemens', 'schneider', 'abb', 'mitsubishi']):
                return 'Automation'
        return 'Unknown'
    
    def _fallback_scan(self, network_range):
        """
        Méthode de fallback utilisant ping si nmap échoue
        
        Args:
            network_range (str): Plage réseau à scanner
            
        Returns:
            list: Liste des appareils détectés
        """
        print("🔄 Utilisation du scan de fallback avec ping...")
        
        devices = []
        base_ip = network_range.split('/')[0]
        base_parts = base_ip.split('.')
        
        # Scanner les 254 premières adresses
        for i in range(1, 255):
            ip = f"{base_parts[0]}.{base_parts[1]}.{base_parts[2]}.{i}"
            
            if self._ping_host(ip):
                device_info = {
                    'ip': ip,
                    'mac': '',
                    'hostname': f"Unknown-{i}",
                    'type': 'Unknown',
                    'scan_time': get_local_time().isoformat(),
                    'is_online': True
                }
                
                # Essayer de récupérer le nom d'hôte
                try:
                    hostname = socket.gethostbyaddr(ip)[0]
                    device_info['hostname'] = hostname
                    device_info['type'] = self._detect_device_type(hostname)
                except:
                    pass
                
                devices.append(device_info)
        
        return devices
    
    def _ping_host(self, ip_address):
        """
        Teste si un hôte répond au ping
        
        Args:
            ip_address (str): Adresse IP à tester
            
        Returns:
            bool: True si l'hôte répond
        """
        try:
            # Paramètres de ping selon le système d'exploitation
            if platform.system().lower() == "windows":
                ping_cmd = [r'C:\Windows\System32\ping.exe', '-n', '1', '-w', '1000', ip_address]
            else:
                ping_cmd = ['ping', '-c', '1', '-W', '1', ip_address]
            
            result = subprocess.run(
                ping_cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=2
            )
            
            return result.returncode == 0
            
        except:
            return False
    
    def scan_single_device(self, ip_address):
        """
        Scanne un appareil spécifique
        
        Args:
            ip_address (str): Adresse IP de l'appareil
            
        Returns:
            dict: Informations de l'appareil ou None si non trouvé
        """
        try:
            # Vérifier si l'appareil répond
            if not self._ping_host(ip_address):
                return None
            
            return self._get_device_info(ip_address)
            
        except Exception as e:
            print(f"❌ Erreur lors du scan de {ip_address}: {str(e)}")
            return None
    
    def get_network_info(self, network_range):
        """
        Récupère des informations sur le réseau
        
        Args:
            network_range (str): Plage réseau
            
        Returns:
            dict: Informations sur le réseau
        """
        try:
            # Extraire les informations de la plage réseau
            if '/' in network_range:
                ip, cidr = network_range.split('/')
                cidr = int(cidr)
                
                # Calculer le masque de sous-réseau
                mask = (0xffffffff >> (32 - cidr)) << (32 - cidr)
                mask_parts = [
                    (mask >> 24) & 0xff,
                    (mask >> 16) & 0xff,
                    (mask >> 8) & 0xff,
                    mask & 0xff
                ]
                subnet_mask = '.'.join(map(str, mask_parts))
                
                # Calculer le nombre d'adresses
                num_addresses = 2 ** (32 - cidr)
                
                return {
                    'network': network_range,
                    'subnet_mask': subnet_mask,
                    'total_addresses': num_addresses,
                    'usable_addresses': num_addresses - 2  # Réserver broadcast et réseau
                }
            else:
                return {
                    'network': network_range,
                    'subnet_mask': '255.255.255.255',
                    'total_addresses': 1,
                    'usable_addresses': 1
                }
                
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse du réseau: {str(e)}")
            return None
    
    def validate_network_range(self, network_range):
        """
        Valide une plage réseau
        
        Args:
            network_range (str): Plage réseau à valider
            
        Returns:
            bool: True si la plage est valide
        """
        try:
            # Pattern pour valider une plage réseau
            pattern = r'^(\d{1,3}\.){3}\d{1,3}(\/\d{1,2})?$'
            
            if not re.match(pattern, network_range):
                return False
            
            # Valider l'adresse IP
            if '/' in network_range:
                ip_part = network_range.split('/')[0]
            else:
                ip_part = network_range
            
            parts = ip_part.split('.')
            for part in parts:
                if not 0 <= int(part) <= 255:
                    return False
            
            # Valider le CIDR si présent
            if '/' in network_range:
                cidr = int(network_range.split('/')[1])
                if not 0 <= cidr <= 32:
                    return False
            
            return True
            
        except:
            return False
    
    def is_valid_ip_range(self, ip_range):
        """
        Alias pour validate_network_range pour compatibilité
        
        Args:
            ip_range (str): Plage IP à valider
            
        Returns:
            bool: True si la plage est valide
        """
        return self.validate_network_range(ip_range) 