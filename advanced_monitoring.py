#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de Monitoring Avancé - Dashboard Danone
Fonctionnalités : Monitoring de services, ports, détection automatique, géolocalisation
"""

import socket
import threading
import time
import json
import requests
import subprocess
import platform
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Tuple
import nmap
import sqlite3
from dataclasses import dataclass
from config_advanced import MONITORING_CONFIG

@dataclass
class ServiceStatus:
    """Statut d'un service"""
    service_name: str
    port: int
    status: str  # 'up', 'down', 'timeout'
    response_time: float
    last_check: datetime
    error_message: Optional[str] = None

@dataclass
class DeviceLocation:
    """Informations de géolocalisation d'un équipement"""
    ip: str
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    isp: Optional[str] = None
    timezone: Optional[str] = None

@dataclass
class BandwidthUsage:
    """Utilisation de bande passante"""
    device_ip: str
    interface: str
    bytes_sent: int
    bytes_received: int
    packets_sent: int
    packets_received: int
    timestamp: datetime

class AdvancedMonitoring:
    """Classe principale pour le monitoring avancé"""
    
    def __init__(self, db_path: str = "network_monitor.db"):
        self.db_path = db_path
        self.config = MONITORING_CONFIG
        self.nm = nmap.PortScanner()
        self.discovered_devices = set()
        self.service_cache = {}
        self.location_cache = {}
        self.bandwidth_cache = {}
        self.running = False
        self.monitoring_thread = None
        
        # Initialiser la base de données
        self.init_database()
        
    def init_database(self):
        """Initialiser les tables de base de données pour le monitoring avancé"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Table pour les services
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS service_monitoring (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_ip TEXT NOT NULL,
                    service_name TEXT NOT NULL,
                    port INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    response_time REAL,
                    last_check TIMESTAMP,
                    error_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Table pour la géolocalisation
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS device_locations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_ip TEXT UNIQUE NOT NULL,
                    country TEXT,
                    region TEXT,
                    city TEXT,
                    latitude REAL,
                    longitude REAL,
                    isp TEXT,
                    timezone TEXT,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Table pour la bande passante
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bandwidth_usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_ip TEXT NOT NULL,
                    interface TEXT NOT NULL,
                    bytes_sent INTEGER,
                    bytes_received INTEGER,
                    packets_sent INTEGER,
                    packets_received INTEGER,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Table pour les nouveaux équipements détectés
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS discovered_devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip_address TEXT UNIQUE NOT NULL,
                    mac_address TEXT,
                    hostname TEXT,
                    device_type TEXT,
                    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'new'
                )
            ''')
            
            conn.commit()
    
    def start_monitoring(self):
        """Démarrer le monitoring en arrière-plan"""
        if not self.running:
            self.running = True
            self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
            self.monitoring_thread.start()
            print("🔍 Monitoring avancé démarré")
    
    def stop_monitoring(self):
        """Arrêter le monitoring"""
        self.running = False
        if self.monitoring_thread:
            self.monitoring_thread.join()
        print("🔍 Monitoring avancé arrêté")
    
    def _monitoring_loop(self):
        """Boucle principale de monitoring"""
        while self.running:
            try:
                # Vérifier les services
                if self.config['enable_service_monitoring']:
                    self.check_all_services()
                
                # Vérifier les ports
                if self.config['enable_port_monitoring']:
                    self.check_all_ports()
                
                # Détection automatique
                if self.config['auto_discovery']:
                    self.auto_discover_devices()
                
                # Mise à jour géolocalisation
                if self.config['enable_geolocation']:
                    self.update_device_locations()
                
                # Monitoring bande passante
                if self.config['enable_bandwidth_monitoring']:
                    self.monitor_bandwidth()
                
                # Attendre l'intervalle configuré
                time.sleep(self.config['discovery_interval'])
                
            except Exception as e:
                print(f"❌ Erreur dans la boucle de monitoring: {e}")
                time.sleep(60)  # Attendre 1 minute en cas d'erreur
    
    def check_service(self, host: str, service_name: str, port: int, timeout: int = 5) -> ServiceStatus:
        """Vérifier le statut d'un service spécifique"""
        start_time = time.time()
        status = "down"
        response_time = None
        error_message = None
        
        try:
            # Créer un socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            # Tenter la connexion
            result = sock.connect_ex((host, port))
            response_time = time.time() - start_time
            
            if result == 0:
                status = "up"
                
                # Tests spécifiques selon le service
                if service_name == "http":
                    status = self._test_http_service(host, port, timeout)
                elif service_name == "https":
                    status = self._test_https_service(host, port, timeout)
                elif service_name == "ftp":
                    status = self._test_ftp_service(host, port, timeout)
                elif service_name == "ssh":
                    status = self._test_ssh_service(host, port, timeout)
                elif service_name == "smtp":
                    status = self._test_smtp_service(host, port, timeout)
                elif service_name == "dns":
                    status = self._test_dns_service(host, port, timeout)
                elif service_name == "snmp":
                    status = self._test_snmp_service(host, port, timeout)
                    
            else:
                error_message = f"Connexion échouée (code: {result})"
                
        except socket.timeout:
            status = "timeout"
            error_message = "Timeout de connexion"
        except Exception as e:
            error_message = str(e)
        finally:
            try:
                sock.close()
            except:
                pass
        
        service_status = ServiceStatus(
            service_name=service_name,
            port=port,
            status=status,
            response_time=response_time,
            last_check=datetime.now(),
            error_message=error_message
        )
        
        # Mettre en cache
        cache_key = f"{host}:{port}:{service_name}"
        self.service_cache[cache_key] = service_status
        
        return service_status
    
    def _test_http_service(self, host: str, port: int, timeout: int) -> str:
        """Test spécifique pour HTTP"""
        try:
            url = f"http://{host}:{port}"
            response = requests.get(url, timeout=timeout, allow_redirects=False)
            if response.status_code < 500:
                return "up"
            else:
                return "down"
        except:
            return "down"
    
    def _test_https_service(self, host: str, port: int, timeout: int) -> str:
        """Test spécifique pour HTTPS"""
        try:
            url = f"https://{host}:{port}"
            response = requests.get(url, timeout=timeout, allow_redirects=False, verify=False)
            if response.status_code < 500:
                return "up"
            else:
                return "down"
        except:
            return "down"
    
    def _test_ftp_service(self, host: str, port: int, timeout: int) -> str:
        """Test spécifique pour FTP"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, port))
            
            # Lire la réponse du serveur FTP
            response = sock.recv(1024).decode('utf-8', errors='ignore')
            sock.close()
            
            if response.startswith('220'):
                return "up"
            else:
                return "down"
        except:
            return "down"
    
    def _test_ssh_service(self, host: str, port: int, timeout: int) -> str:
        """Test spécifique pour SSH"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, port))
            
            # Lire la bannière SSH
            response = sock.recv(1024).decode('utf-8', errors='ignore')
            sock.close()
            
            if 'SSH' in response:
                return "up"
            else:
                return "down"
        except:
            return "down"
    
    def _test_smtp_service(self, host: str, port: int, timeout: int) -> str:
        """Test spécifique pour SMTP"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, port))
            
            # Lire la réponse du serveur SMTP
            response = sock.recv(1024).decode('utf-8', errors='ignore')
            sock.close()
            
            if response.startswith('220'):
                return "up"
            else:
                return "down"
        except:
            return "down"
    
    def _test_dns_service(self, host: str, port: int, timeout: int) -> str:
        """Test spécifique pour DNS"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, port))
            
            # Envoyer une requête DNS simple
            dns_query = b'\x00\x01\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x03com\x00\x00\x01\x00\x01'
            sock.send(dns_query)
            
            # Lire la réponse
            response = sock.recv(1024)
            sock.close()
            
            if len(response) > 0:
                return "up"
            else:
                return "down"
        except:
            return "down"
    
    def _test_snmp_service(self, host: str, port: int, timeout: int) -> str:
        """Test spécifique pour SNMP"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, port))
            
            # Envoyer une requête SNMP simple (GetRequest)
            snmp_request = b'\x30\x1c\x02\x01\x01\x04\x06public\xa0\x0f\x02\x01\x01\x02\x01\x00\x02\x01\x00\x30\x04\x30\x02\x06\x00'
            sock.send(snmp_request)
            
            # Lire la réponse
            response = sock.recv(1024)
            sock.close()
            
            if len(response) > 0:
                return "up"
            else:
                return "down"
        except:
            return "down"
    
    def check_all_services(self):
        """Vérifier tous les services configurés"""
        print("🔍 Vérification des services...")
        
        # Récupérer tous les équipements de la base
        devices = self.get_all_devices()
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            
            for device in devices:
                for service_name, service_config in self.config['monitored_services'].items():
                    future = executor.submit(
                        self.check_service,
                        device['ip'],
                        service_name,
                        service_config['port'],
                        service_config['timeout']
                    )
                    futures.append(future)
            
            # Collecter les résultats
            for future in as_completed(futures):
                try:
                    service_status = future.result()
                    self.save_service_status(service_status)
                except Exception as e:
                    print(f"❌ Erreur lors de la vérification de service: {e}")
    
    def check_all_ports(self):
        """Vérifier tous les ports configurés"""
        print("🔌 Vérification des ports...")
        
        devices = self.get_all_devices()
        
        for device in devices:
            try:
                # Utiliser nmap pour scanner les ports
                scan_result = self.nm.scan(device['ip'], arguments='-sS -T4 -p ' + ','.join(map(str, self.config['monitored_ports'])))
                
                if device['ip'] in scan_result['scan']:
                    host_result = scan_result['scan'][device['ip']]
                    
                    for port in self.config['monitored_ports']:
                        port_str = str(port)
                        if 'tcp' in host_result and port_str in host_result['tcp']:
                            port_status = host_result['tcp'][port_str]['state']
                            
                            service_status = ServiceStatus(
                                service_name=f"port_{port}",
                                port=port,
                                status="up" if port_status == "open" else "down",
                                response_time=None,
                                last_check=datetime.now()
                            )
                            
                            self.save_service_status(service_status)
                            
            except Exception as e:
                print(f"❌ Erreur lors du scan de ports pour {device['ip']}: {e}")
    
    def auto_discover_devices(self):
        """Détection automatique de nouveaux équipements"""
        print("🆕 Détection automatique d'équipements...")
        
        try:
            # Scanner le réseau pour découvrir de nouveaux équipements
            network_range = "192.168.1.0/24"  # À configurer
            
            scan_result = self.nm.scan(hosts=network_range, arguments='-sn')
            
            for host in scan_result['scan']:
                if scan_result['scan'][host]['status']['state'] == 'up':
                    # Vérifier si c'est un nouvel équipement
                    if host not in self.discovered_devices:
                        self.discovered_devices.add(host)
                        
                        # Récupérer les informations de l'équipement
                        host_info = scan_result['scan'][host]
                        
                        # Détecter le type d'équipement
                        device_type = self._detect_device_type(host, host_info)
                        
                        # Sauvegarder le nouvel équipement
                        self.save_discovered_device(host, host_info, device_type)
                        
                        print(f"🆕 Nouvel équipement détecté: {host} ({device_type})")
        
        except Exception as e:
            print(f"❌ Erreur lors de la détection automatique: {e}")
    
    def _detect_device_type(self, ip: str, host_info: dict) -> str:
        """Détecter le type d'équipement basé sur les informations nmap"""
        try:
            # Vérifier les ports ouverts pour déterminer le type
            if 'tcp' in host_info:
                open_ports = [port for port, data in host_info['tcp'].items() if data['state'] == 'open']
                
                # Logique de détection basée sur les ports
                if 80 in open_ports or 443 in open_ports:
                    return "web_server"
                elif 22 in open_ports:
                    return "server"
                elif 21 in open_ports:
                    return "ftp_server"
                elif 25 in open_ports or 587 in open_ports:
                    return "mail_server"
                elif 53 in open_ports:
                    return "dns_server"
                elif 3389 in open_ports:
                    return "windows_pc"
                elif 5900 in open_ports:
                    return "vnc_server"
                else:
                    return "unknown"
            else:
                return "unknown"
                
        except Exception as e:
            print(f"❌ Erreur lors de la détection du type d'équipement: {e}")
            return "unknown"
    
    def get_device_location(self, ip: str) -> Optional[DeviceLocation]:
        """Obtenir la géolocalisation d'un équipement"""
        # Vérifier le cache
        if ip in self.location_cache:
            return self.location_cache[ip]
        
        try:
            # Utiliser un service de géolocalisation IP
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                if data['status'] == 'success':
                    location = DeviceLocation(
                        ip=ip,
                        country=data.get('country'),
                        region=data.get('regionName'),
                        city=data.get('city'),
                        latitude=data.get('lat'),
                        longitude=data.get('lon'),
                        isp=data.get('isp'),
                        timezone=data.get('timezone')
                    )
                    
                    # Mettre en cache
                    self.location_cache[ip] = location
                    
                    # Sauvegarder en base
                    self.save_device_location(location)
                    
                    return location
            
        except Exception as e:
            print(f"❌ Erreur lors de la géolocalisation de {ip}: {e}")
        
        return None
    
    def update_device_locations(self):
        """Mettre à jour les géolocalisations de tous les équipements"""
        print("🌍 Mise à jour des géolocalisations...")
        
        devices = self.get_all_devices()
        
        for device in devices:
            location = self.get_device_location(device['ip'])
            if location:
                print(f"📍 {device['ip']} -> {location.city}, {location.country}")
    
    def monitor_bandwidth(self):
        """Monitorer l'utilisation de bande passante"""
        print("📊 Monitoring de la bande passante...")
        
        try:
            # Utiliser les commandes système pour obtenir les statistiques réseau
            if platform.system() == "Windows":
                self._monitor_bandwidth_windows()
            else:
                self._monitor_bandwidth_linux()
                
        except Exception as e:
            print(f"❌ Erreur lors du monitoring de bande passante: {e}")
    
    def _monitor_bandwidth_windows(self):
        """Monitoring de bande passante sur Windows"""
        try:
            # Utiliser netstat pour obtenir les statistiques
            result = subprocess.run(['netstat', '-e'], capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'Bytes' in line and 'Sent' in line:
                        parts = line.split()
                        if len(parts) >= 4:
                            bytes_sent = int(parts[1])
                            bytes_received = int(parts[2])
                            
                            # Sauvegarder les statistiques
                            self.save_bandwidth_usage("localhost", "default", bytes_sent, bytes_received, 0, 0)
                            break
                            
        except Exception as e:
            print(f"❌ Erreur monitoring Windows: {e}")
    
    def _monitor_bandwidth_linux(self):
        """Monitoring de bande passante sur Linux"""
        try:
            # Lire /proc/net/dev pour obtenir les statistiques
            with open('/proc/net/dev', 'r') as f:
                lines = f.readlines()
                
            for line in lines[2:]:  # Ignorer les en-têtes
                parts = line.split()
                if len(parts) >= 10:
                    interface = parts[0].rstrip(':')
                    bytes_received = int(parts[1])
                    packets_received = int(parts[2])
                    bytes_sent = int(parts[9])
                    packets_sent = int(parts[10])
                    
                    # Sauvegarder les statistiques
                    self.save_bandwidth_usage("localhost", interface, bytes_sent, bytes_received, packets_sent, packets_received)
                    
        except Exception as e:
            print(f"❌ Erreur monitoring Linux: {e}")
    
    def get_all_devices(self) -> List[Dict]:
        """Récupérer tous les équipements de la base de données"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, ip, mac, hostname, device_type FROM devices')
            devices = []
            for row in cursor.fetchall():
                devices.append({
                    'id': row[0],
                    'ip': row[1],
                    'mac': row[2],
                    'hostname': row[3],
                    'device_type': row[4]
                })
            return devices
    
    def save_service_status(self, service_status: ServiceStatus):
        """Sauvegarder le statut d'un service"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO service_monitoring 
                (device_ip, service_name, port, status, response_time, last_check, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                service_status.service_name.split(':')[0] if ':' in service_status.service_name else 'localhost',
                service_status.service_name,
                service_status.port,
                service_status.status,
                service_status.response_time,
                service_status.last_check,
                service_status.error_message
            ))
            conn.commit()
    
    def save_discovered_device(self, ip: str, host_info: dict, device_type: str):
        """Sauvegarder un nouvel équipement découvert"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Récupérer le MAC address si disponible
            mac_address = None
            if 'addresses' in host_info and 'mac' in host_info['addresses']:
                mac_address = host_info['addresses']['mac']
            
            # Récupérer le hostname si disponible
            hostname = None
            if 'hostnames' in host_info and host_info['hostnames']:
                hostname = host_info['hostnames'][0]['name']
            
            cursor.execute('''
                INSERT OR REPLACE INTO discovered_devices 
                (ip_address, mac_address, hostname, device_type, last_seen, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (ip, mac_address, hostname, device_type, datetime.now(), 'active'))
            
            conn.commit()
    
    def save_device_location(self, location: DeviceLocation):
        """Sauvegarder la géolocalisation d'un équipement"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO device_locations 
                (device_ip, country, region, city, latitude, longitude, isp, timezone, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                location.ip, location.country, location.region, location.city,
                location.latitude, location.longitude, location.isp, location.timezone,
                datetime.now()
            ))
            conn.commit()
    
    def save_bandwidth_usage(self, device_ip: str, interface: str, bytes_sent: int, 
                           bytes_received: int, packets_sent: int, packets_received: int):
        """Sauvegarder l'utilisation de bande passante"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO bandwidth_usage 
                (device_ip, interface, bytes_sent, bytes_received, packets_sent, packets_received)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (device_ip, interface, bytes_sent, bytes_received, packets_sent, packets_received))
            conn.commit()
    
    def get_service_status_summary(self) -> Dict:
        """Obtenir un résumé des statuts de services"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT service_name, status, COUNT(*) as count
                FROM service_monitoring 
                WHERE last_check > datetime('now', '-1 hour')
                GROUP BY service_name, status
            ''')
            
            summary = {}
            for row in cursor.fetchall():
                service_name, status, count = row
                if service_name not in summary:
                    summary[service_name] = {}
                summary[service_name][status] = count
            
            return summary
    
    def get_discovered_devices(self) -> List[Dict]:
        """Obtenir la liste des équipements découverts"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT ip_address, mac_address, hostname, device_type, 
                       first_seen, last_seen, status
                FROM discovered_devices
                ORDER BY last_seen DESC
            ''')
            
            devices = []
            for row in cursor.fetchall():
                devices.append({
                    'ip': row[0],
                    'mac': row[1],
                    'hostname': row[2],
                    'device_type': row[3],
                    'first_seen': row[4],
                    'last_seen': row[5],
                    'status': row[6]
                })
            
            return devices
    
    def get_device_locations(self) -> List[DeviceLocation]:
        """Obtenir toutes les géolocalisations"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT device_ip, country, region, city, latitude, longitude, isp, timezone
                FROM device_locations
            ''')
            
            locations = []
            for row in cursor.fetchall():
                locations.append(DeviceLocation(
                    ip=row[0],
                    country=row[1],
                    region=row[2],
                    city=row[3],
                    latitude=row[4],
                    longitude=row[5],
                    isp=row[6],
                    timezone=row[7]
                ))
            
            return locations

# Instance globale
advanced_monitoring = AdvancedMonitoring() 