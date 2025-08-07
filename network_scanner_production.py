#!/usr/bin/env python3
"""
Scanner Réseau Professionnel - Production Ready
Détection réelle des équipements réseau avec informations détaillées
"""

import nmap
import socket
import subprocess
import platform
import re
import threading
import time
import json
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

# Configuration du PATH pour Nmap sur Windows
if platform.system() == "Windows":
    nmap_paths = [
        r"C:\Program Files (x86)\Nmap",
        r"C:\Program Files\Nmap"
    ]
    for path in nmap_paths:
        if os.path.exists(path) and path not in os.environ["PATH"]:
            os.environ["PATH"] += os.pathsep + path

def get_local_time():
    """Retourne l'heure locale actuelle"""
    return datetime.now()

class ProductionNetworkScanner:
    """Scanner réseau professionnel pour environnement de production"""
    
    def __init__(self):
        self.nm = None
        self.nmap_available = False
        self.mac_vendors = {}
        
        # Initialiser Nmap
        try:
            self.nm = nmap.PortScanner()
            self.nmap_available = True
            print("✅ Nmap initialisé avec succès")
        except Exception as e:
            print(f"❌ Erreur initialisation Nmap: {e}")
            print("⚠️ Mode fallback activé")
        
        # Base de données des types d'équipements (étendue)
        self.device_signatures = {
            'router': {
                'hostnames': ['router', 'rt-', 'gw-', 'gateway', 'firewall', 'fw-', 'pfsense', 'opnsense'],
                'vendors': ['cisco', 'netgear', 'linksys', 'asus', 'tp-link', 'dlink', 'ubiquiti'],
                'ports': [22, 23, 80, 443, 8080, 8443]
            },
            'switch': {
                'hostnames': ['switch', 'sw-', 'hub'],
                'vendors': ['cisco', 'hp', 'dell', 'netgear', 'tp-link'],
                'ports': [22, 23, 80, 443, 161, 8080]
            },
            'server': {
                'hostnames': ['server', 'srv', 'dc-', 'ad-', 'dns-', 'dhcp-', 'web-', 'mail-', 'db-'],
                'vendors': ['dell', 'hp', 'lenovo', 'supermicro', 'intel'],
                'ports': [22, 80, 443, 3389, 5985, 5986, 25, 993, 1433, 3306]
            },
            'printer': {
                'hostnames': ['printer', 'print', 'hp-', 'canon-', 'epson-', 'brother-'],
                'vendors': ['hewlett packard', 'canon', 'epson', 'brother', 'lexmark', 'xerox'],
                'ports': [80, 443, 515, 631, 9100]
            },
            'nas': {
                'hostnames': ['nas-', 'storage-', 'synology-', 'qnap-'],
                'vendors': ['synology', 'qnap', 'netgear', 'buffalo'],
                'ports': [80, 443, 22, 21, 139, 445, 5000, 5001]
            },
            'camera': {
                'hostnames': ['camera', 'cam-', 'ipcam-', 'cctv-'],
                'vendors': ['hikvision', 'dahua', 'axis', 'bosch', 'samsung'],
                'ports': [80, 443, 554, 8080, 8000]
            },
            'phone': {
                'hostnames': ['phone-', 'voip-', 'sip-', 'tel-'],
                'vendors': ['cisco', 'polycom', 'yealink', 'grandstream', 'avaya'],
                'ports': [80, 443, 5060, 5061, 8080]
            },
            'automation': {
                'hostnames': ['plc-', 'hmi-', 'scada-', 'automate-'],
                'vendors': ['siemens', 'schneider', 'allen bradley', 'omron'],
                'ports': [80, 443, 102, 502, 44818]
            },
            'workstation': {
                'hostnames': ['pc-', 'ws-', 'desktop-', 'laptop-', 'poste-'],
                'vendors': ['dell', 'hp', 'lenovo', 'asus', 'acer'],
                'ports': [135, 139, 445, 3389, 5985]
            }
        }
        
        # Charger la base des vendors MAC (OUI)
        self._load_mac_vendors()
    
    def _load_mac_vendors(self):
        """Charge la base de données des vendors MAC"""
        try:
            # Essayer de charger depuis un fichier local
            if os.path.exists('oui_vendors.json'):
                with open('oui_vendors.json', 'r') as f:
                    self.mac_vendors = json.load(f)
                print("✅ Base vendors MAC chargée (fichier local)")
                return
                
            # Sinon, utiliser une base simplifiée
            self.mac_vendors = {
                "00:00:5E": "IANA",
                "00:50:56": "VMware",
                "08:00:27": "Oracle VirtualBox",
                "00:0C:29": "VMware",
                "00:1B:21": "Intel",
                "00:E0:4C": "Realtek",
                "00:90:F5": "Cisco",
                "00:1F:45": "Netgear",
                "B8:27:EB": "Raspberry Pi",
                "DC:A6:32": "Raspberry Pi",
                "28:C6:8E": "TP-Link",
                "F4:F2:6D": "Samsung",
                # Ajouter plus si nécessaire
            }
            print("✅ Base vendors MAC simplifiée chargée")
            
        except Exception as e:
            print(f"⚠️ Erreur chargement vendors MAC: {e}")
            self.mac_vendors = {}
    
    def discover_local_networks(self):
        """Découvre automatiquement les réseaux locaux"""
        networks = []
        
        try:
            if platform.system() == "Windows":
                # Windows - utiliser ipconfig
                result = subprocess.run(['ipconfig'], capture_output=True, text=True, shell=True)
                output = result.stdout
                
                # Parser les interfaces réseau
                interfaces = []
                current_interface = None
                
                for line in output.split('\n'):
                    line = line.strip()
                    if 'adapter' in line.lower() and ':' in line:
                        current_interface = line
                    elif 'IPv4' in line and current_interface:
                        ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                        if ip_match:
                            ip = ip_match.group(1)
                            # Calculer le réseau /24
                            ip_parts = ip.split('.')
                            network = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
                            
                            interfaces.append({
                                'interface': current_interface,
                                'ip': ip,
                                'network': network
                            })
                
                # Ajouter les réseaux découverts
                for interface in interfaces:
                    if not any(n['network'] == interface['network'] for n in networks):
                        networks.append({
                            'interface': interface['interface'],
                            'network': interface['network'],
                            'local_ip': interface['ip'],
                            'auto_detected': True
                        })
            
            else:
                # Linux/Mac - utiliser ip route ou route
                try:
                    result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
                    output = result.stdout
                except:
                    result = subprocess.run(['route', '-n'], capture_output=True, text=True)
                    output = result.stdout
                
                # Parser les routes
                for line in output.split('\n'):
                    if '/' in line and 'link' in line.lower():
                        parts = line.split()
                        if len(parts) > 0 and '/' in parts[0]:
                            network = parts[0]
                            networks.append({
                                'interface': 'auto-detected',
                                'network': network,
                                'auto_detected': True
                            })
        
        except Exception as e:
            print(f"⚠️ Erreur découverte réseaux: {e}")
            # Fallback - réseaux communs
            networks = [
                {'interface': 'fallback', 'network': '192.168.1.0/24', 'auto_detected': False},
                {'interface': 'fallback', 'network': '192.168.0.0/24', 'auto_detected': False},
                {'interface': 'fallback', 'network': '10.0.0.0/24', 'auto_detected': False}
            ]
        
        print(f"🔍 {len(networks)} réseau(x) découvert(s)")
        for net in networks:
            status = "✅ Auto" if net.get('auto_detected') else "⚠️ Fallback"
            print(f"  {status}: {net['network']}")
        
        return networks
    
    def scan_network_advanced(self, network_range, aggressive=False):
        """
        Scan réseau avancé avec détection détaillée des équipements
        
        Args:
            network_range (str): Réseau à scanner (ex: "192.168.1.0/24")
            aggressive (bool): Mode agressif avec scan de ports
            
        Returns:
            list: Liste des équipements détectés avec informations complètes
        """
        print(f"🚀 Scan avancé du réseau {network_range}")
        start_time = time.time()
        devices = []
        
        if not self.nmap_available:
            print("❌ Nmap non disponible - scan limité")
            return self._fallback_ping_scan(network_range)
        
        try:
            # Phase 1: Découverte des hôtes actifs
            print("📡 Phase 1: Découverte des hôtes...")
            discovery_args = '-sn -PE -PP -PM -n --max-retries 2 --host-timeout 30s'
            
            scan_result = self.nm.scan(hosts=network_range, arguments=discovery_args)
            active_hosts = [host for host in self.nm.all_hosts() if self.nm[host].state() == 'up']
            
            print(f"✅ {len(active_hosts)} hôte(s) actif(s) découvert(s)")
            
            # Phase 2: Scan détaillé de chaque hôte
            print("🔍 Phase 2: Analyse détaillée...")
            
            for host in active_hosts:
                device_info = self._analyze_host_detailed(host, aggressive)
                if device_info:
                    devices.append(device_info)
                    print(f"  ✅ {host}: {device_info['type']} - {device_info['hostname']}")
        
        except Exception as e:
            print(f"❌ Erreur scan avancé: {e}")
            return self._fallback_ping_scan(network_range)
        
        scan_duration = time.time() - start_time
        print(f"🎯 Scan terminé en {scan_duration:.2f}s - {len(devices)} équipements détectés")
        
        return devices
    
    def _analyze_host_detailed(self, ip_address, aggressive=False):
        """Analyse détaillée d'un hôte"""
        try:
            device_info = {
                'ip': ip_address,
                'hostname': '',
                'mac': '',
                'mac_vendor': '',
                'type': 'Unknown',
                'os': '',
                'ports': [],
                'services': [],
                'response_time': 0.0,
                'confidence': 0,
                'last_seen': get_local_time().isoformat(),
                'is_online': True
            }
            
            # 1. Résolution DNS inverse
            try:
                hostname_info = socket.gethostbyaddr(ip_address)
                device_info['hostname'] = hostname_info[0]
            except:
                device_info['hostname'] = f"device-{ip_address.split('.')[-1]}"
            
            # 2. Informations MAC (si local)
            if ip_address in self.nm.all_hosts():
                host_info = self.nm[ip_address]
                addresses = host_info.get('addresses', {})
                device_info['mac'] = addresses.get('mac', '')
                
                # Vendor MAC
                if device_info['mac']:
                    mac_prefix = device_info['mac'][:8].upper()
                    device_info['mac_vendor'] = self.mac_vendors.get(mac_prefix, 'Unknown')
            
            # 3. Scan de ports (si mode agressif)
            if aggressive:
                device_info['ports'], device_info['services'] = self._scan_common_ports(ip_address)
            
            # 4. Détection du type d'équipement
            device_info['type'], device_info['confidence'] = self._detect_device_type_advanced(
                device_info['hostname'], 
                device_info['mac_vendor'], 
                device_info['ports']
            )
            
            # 5. Estimation de l'OS (si possible)
            device_info['os'] = self._guess_os(device_info['hostname'], device_info['ports'])
            
            # 6. Mesure du temps de réponse
            device_info['response_time'] = self._measure_response_time(ip_address)
            
            return device_info
            
        except Exception as e:
            print(f"❌ Erreur analyse {ip_address}: {e}")
            return None
    
    def _scan_common_ports(self, ip_address):
        """Scan des ports communs"""
        common_ports = "22,23,25,53,80,110,143,443,993,995,1433,3306,3389,5432,5985,5986,8080,8443,9100"
        
        try:
            scan_result = self.nm.scan(
                hosts=ip_address, 
                ports=common_ports, 
                arguments='-sS --max-retries 1 --host-timeout 10s'
            )
            
            ports = []
            services = []
            
            if ip_address in self.nm.all_hosts():
                for proto in self.nm[ip_address].all_protocols():
                    ports_info = self.nm[ip_address][proto].keys()
                    for port in ports_info:
                        port_state = self.nm[ip_address][proto][port]['state']
                        if port_state == 'open':
                            ports.append(port)
                            service = self.nm[ip_address][proto][port].get('name', 'unknown')
                            services.append(f"{port}/{service}")
            
            return ports, services
            
        except Exception as e:
            print(f"⚠️ Erreur scan ports {ip_address}: {e}")
            return [], []
    
    def _detect_device_type_advanced(self, hostname, mac_vendor, ports):
        """Détection avancée du type d'équipement"""
        scores = {}
        hostname_lower = hostname.lower()
        vendor_lower = mac_vendor.lower() if mac_vendor else ''
        
        # Analyser chaque type d'équipement
        for device_type, signatures in self.device_signatures.items():
            score = 0
            
            # Score basé sur le hostname
            for pattern in signatures['hostnames']:
                if pattern in hostname_lower:
                    score += 30
                    break
            
            # Score basé sur le vendor MAC
            for vendor in signatures['vendors']:
                if vendor in vendor_lower:
                    score += 25
                    break
            
            # Score basé sur les ports ouverts
            if ports:
                matching_ports = set(ports) & set(signatures['ports'])
                if matching_ports:
                    score += len(matching_ports) * 15
            
            scores[device_type] = score
        
        # Déterminer le type avec le meilleur score
        if scores:
            best_type = max(scores.keys(), key=lambda k: scores[k])
            confidence = min(scores[best_type], 100)
            
            if confidence > 20:
                return best_type, confidence
        
        return 'Unknown', 0
    
    def _guess_os(self, hostname, ports):
        """Estimation de l'OS basée sur les indices"""
        hostname_lower = hostname.lower()
        
        # Indices Windows
        if any(keyword in hostname_lower for keyword in ['pc-', 'ws-', 'desktop-', 'laptop-']):
            if 3389 in ports or 5985 in ports:
                return 'Windows'
        
        # Indices Linux
        if 22 in ports and 80 in ports:
            return 'Linux'
        
        # Indices Network devices
        if any(keyword in hostname_lower for keyword in ['router', 'switch', 'gw-']):
            return 'Network Device'
        
        return 'Unknown'
    
    def _measure_response_time(self, ip_address):
        """Mesure le temps de réponse ping"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ['ping', '-n', '3', ip_address], 
                    capture_output=True, text=True, timeout=10
                )
                
                # Parser le temps de réponse
                for line in result.stdout.split('\n'):
                    if 'time=' in line.lower():
                        time_match = re.search(r'time[=<](\d+)ms', line.lower())
                        if time_match:
                            return float(time_match.group(1))
            else:
                result = subprocess.run(
                    ['ping', '-c', '3', ip_address], 
                    capture_output=True, text=True, timeout=10
                )
                
                # Parser pour Linux/Mac
                for line in result.stdout.split('\n'):
                    if 'time=' in line:
                        time_match = re.search(r'time=(\d+\.?\d*)ms', line)
                        if time_match:
                            return float(time_match.group(1))
            
            return 0.0
            
        except:
            return 0.0
    
    def _fallback_ping_scan(self, network_range):
        """Scan de fallback avec ping simple"""
        print("🔄 Mode fallback: scan ping simple")
        devices = []
        
        try:
            # Calculer la plage d'IPs
            if '/' in network_range:
                network_ip = network_range.split('/')[0]
                base_ip = '.'.join(network_ip.split('.')[:-1])
                
                # Scanner les 254 adresses possibles
                def ping_ip(i):
                    ip = f"{base_ip}.{i}"
                    if self._ping_host_simple(ip):
                        return self._get_basic_info(ip)
                    return None
                
                # Utiliser des threads pour accélérer
                with ThreadPoolExecutor(max_workers=50) as executor:
                    futures = [executor.submit(ping_ip, i) for i in range(1, 255)]
                    
                    for future in as_completed(futures):
                        result = future.result()
                        if result:
                            devices.append(result)
                            print(f"  ✅ {result['ip']}: {result['hostname']}")
            
        except Exception as e:
            print(f"❌ Erreur scan fallback: {e}")
        
        return devices
    
    def _ping_host_simple(self, ip_address):
        """Ping simple d'un hôte"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ['ping', '-n', '1', '-w', '3000', ip_address], 
                    capture_output=True, timeout=5
                )
            else:
                result = subprocess.run(
                    ['ping', '-c', '1', '-W', '3', ip_address], 
                    capture_output=True, timeout=5
                )
            
            return result.returncode == 0
            
        except:
            return False
    
    def _get_basic_info(self, ip_address):
        """Récupère les informations de base d'un équipement"""
        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
        except:
            hostname = f"device-{ip_address.split('.')[-1]}"
        
        return {
            'ip': ip_address,
            'hostname': hostname,
            'mac': '',
            'mac_vendor': '',
            'type': 'Unknown',
            'os': '',
            'ports': [],
            'services': [],
            'response_time': 0.0,
            'confidence': 0,
            'last_seen': get_local_time().isoformat(),
            'is_online': True
        }
    
    def scan_all_networks(self, aggressive=False):
        """Scanne tous les réseaux découverts"""
        networks = self.discover_local_networks()
        all_devices = []
        
        print(f"🌐 Scan de {len(networks)} réseau(x)")
        
        for network_info in networks:
            network_range = network_info['network']
            print(f"\n📡 Scan du réseau: {network_range}")
            
            try:
                devices = self.scan_network_advanced(network_range, aggressive)
                all_devices.extend(devices)
                
                print(f"✅ {network_range}: {len(devices)} équipements")
                
            except Exception as e:
                print(f"❌ Erreur scan {network_range}: {e}")
        
        print(f"\n🎯 TOTAL: {len(all_devices)} équipements détectés")
        return all_devices

# Alias pour compatibilité avec l'ancien code
NetworkScanner = ProductionNetworkScanner
