"""
Module d'Intelligence Artificielle pour le Dashboard Central Danone
Intégration complète d'IA pour la supervision réseau
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, IsolationForest, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.cluster import KMeans
import joblib
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeviceClassifier:
    """Classification intelligente des équipements"""
    
    def __init__(self):
        self.label_encoder = LabelEncoder()
        self.classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.device_types = {
            'server': ['server', 'srv', 'dc', 'domain', 'exchange', 'sql', 'web'],
            'router': ['router', 'gateway', 'firewall', 'switch', 'core'],
            'printer': ['printer', 'print', 'hp', 'canon', 'epson'],
            'workstation': ['pc', 'workstation', 'desktop', 'laptop', 'client'],
            'plc': ['plc', 'automation', 'control', 'scada'],
            'camera': ['camera', 'ipcam', 'surveillance'],
            'unknown': ['unknown', 'unknown']
        }
        
    def extract_features(self, hostname: str, mac_vendor: str, ip: str) -> np.ndarray:
        """Extrait les caractéristiques pour la classification"""
        features = []
        
        # Caractéristiques du hostname
        hostname_lower = hostname.lower()
        features.extend([
            len(hostname),
            hostname.count('-'),
            hostname.count('_'),
            hostname.count('.'),
            any(word in hostname_lower for word in ['server', 'srv', 'dc']),
            any(word in hostname_lower for word in ['router', 'gateway', 'firewall']),
            any(word in hostname_lower for word in ['printer', 'print', 'hp']),
            any(word in hostname_lower for word in ['pc', 'workstation', 'desktop']),
            any(word in hostname_lower for word in ['plc', 'automation', 'control']),
            any(word in hostname_lower for word in ['camera', 'ipcam', 'surveillance'])
        ])
        
        # Caractéristiques du MAC vendor
        mac_lower = mac_vendor.lower()
        features.extend([
            len(mac_vendor),
            any(word in mac_lower for word in ['cisco', 'juniper', 'hp', 'dell']),
            any(word in mac_lower for word in ['microsoft', 'apple', 'samsung']),
            any(word in mac_lower for word in ['schneider', 'siemens', 'rockwell'])
        ])
        
        # Caractéristiques de l'IP
        ip_parts = ip.split('.')
        features.extend([
            int(ip_parts[0]),
            int(ip_parts[1]),
            int(ip_parts[2]),
            int(ip_parts[3])
        ])
        
        return np.array(features)
    
    def classify_device(self, hostname: str, mac_vendor: str, ip: str) -> Dict:
        """Classifie un équipement (version enrichie)"""
        try:
            features = self.extract_features(hostname, mac_vendor, ip)
            hostname_lower = hostname.lower() if hostname else ''
            mac_lower = mac_vendor.lower() if mac_vendor else ''

            # Enrichissement des règles de détection
            # Switch/Routeur
            if any(word in hostname_lower for word in ['switch', 'sw', 'hub', 'aruba', 'juniper', 'procurve', 'zyxel', 'tenda', 'h3c', 'fortinet', 'alcatel', 'zte', 'mikrotik', 'ubiquiti', 'linksys']) or any(word in mac_lower for word in ['cisco', 'netgear', 'tplink', 'dlink', 'aruba', 'juniper', 'zyxel', 'tenda', 'h3c', 'fortinet', 'alcatel', 'zte', 'huawei', 'mikrotik', 'ubiquiti', 'linksys']):
                device_type = 'switch'
                confidence = 0.92
            # Téléphone
            elif any(word in hostname_lower for word in ['phone', 'voip', 'sip', 'polycom', 'yealink', 'avaya', 'iphone', 'android', 'samsung', 'huawei', 'xiaomi', 'oneplus', 'itel', 'ipad', 'tablet', 'oppo', 'vivo']) or any(word in mac_lower for word in ['apple', 'samsung', 'huawei', 'xiaomi', 'oneplus', 'itel', 'polycom', 'yealink', 'avaya', 'cisco', 'oppo', 'vivo']):
                device_type = 'phone'
                confidence = 0.91
            # Imprimante
            elif any(word in hostname_lower for word in ['printer', 'print', 'hp', 'canon', 'epson', 'brother', 'xerox', 'ricoh', 'lexmark', 'kyocera']) or any(word in mac_lower for word in ['hp', 'canon', 'epson', 'brother', 'xerox', 'ricoh', 'lexmark', 'kyocera']):
                device_type = 'printer'
                confidence = 0.90
            # Box/Modem
            elif any(word in hostname_lower for word in ['box', 'modem', 'livebox', 'bbox', 'freebox', 'sfrbox', 'zte', 'huawei', 'sagem', 'technicolor']) or any(word in mac_lower for word in ['zte', 'huawei', 'sagem', 'technicolor', 'livebox', 'bbox', 'freebox', 'sfrbox']):
                device_type = 'box'
                confidence = 0.90
            # PLC/Automate
            elif any(word in hostname_lower for word in ['plc', 'automation', 'automate', 'scada', 'hmi', 'control', 'abb', 'mitsubishi', 'omron']) or any(word in mac_lower for word in ['siemens', 'schneider', 'abb', 'mitsubishi', 'omron']):
                device_type = 'plc'
                confidence = 0.89
            # Caméra
            elif any(word in hostname_lower for word in ['camera', 'ipcam', 'surveillance', 'hikvision', 'dahua', 'foscam', 'arlo', 'axis']) or any(word in mac_lower for word in ['hikvision', 'dahua', 'foscam', 'arlo', 'axis']):
                device_type = 'camera'
                confidence = 0.88
            # Serveur
            elif any(word in hostname_lower for word in ['server', 'srv', 'dc', 'domain', 'exchange', 'sql', 'web', 'nas', 'synology', 'qnap']) or any(word in mac_lower for word in ['synology', 'qnap', 'nas', 'dell', 'hp', 'ibm', 'lenovo']):
                device_type = 'server'
                confidence = 0.95
            # PC/Workstation
            elif any(word in hostname_lower for word in ['pc', 'workstation', 'desktop', 'laptop', 'client', 'lenovo', 'dell', 'asus', 'acer', 'msi', 'hp', 'windows', 'macbook', 'imac']) or any(word in mac_lower for word in ['lenovo', 'dell', 'asus', 'acer', 'msi', 'hp', 'windows', 'macbook', 'imac']):
                device_type = 'workstation'
                confidence = 0.85
            # Routeur (fallback)
            elif any(word in hostname_lower for word in ['router', 'gateway', 'firewall', 'core']) or any(word in mac_lower for word in ['cisco', 'netgear', 'tplink', 'dlink', 'aruba', 'juniper', 'zyxel', 'tenda', 'h3c', 'fortinet', 'alcatel', 'zte', 'huawei', 'mikrotik', 'ubiquiti', 'linksys']):
                device_type = 'router'
                confidence = 0.90
            # Fallback box sur IP .1 ou .254
            elif ip.endswith('.1') or ip.endswith('.254'):
                if any(word in mac_lower for word in ['zte', 'huawei', 'sagem', 'technicolor', 'livebox', 'bbox', 'freebox', 'sfrbox']):
                    device_type = 'box'
                    confidence = 0.88
                else:
                    device_type = 'router'
                    confidence = 0.80
            else:
                device_type = 'unknown'
                confidence = 0.60
            return {
                'device_type': device_type,
                'confidence': confidence,
                'features': features.tolist()
            }
        except Exception as e:
            logger.error(f"Erreur classification: {e}")
            return {'device_type': 'unknown', 'confidence': 0.0, 'features': []}

class AnomalyDetector:
    """Détection d'anomalies réseau"""
    
    def __init__(self):
        self.isolation_forest = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.is_fitted = False
        
    def extract_anomaly_features(self, device_history: List[Dict]) -> np.ndarray:
        """Extrait les caractéristiques pour la détection d'anomalies"""
        if not device_history:
            return np.array([])
        
        features = []
        for record in device_history[-50:]:  # Derniers 50 enregistrements
            feature_vector = [
                record.get('response_time', 0),
                record.get('packet_loss', 0),
                record.get('is_online', 1),
                record.get('scan_duration', 0),
                record.get('error_count', 0)
            ]
            features.append(feature_vector)
        
        return np.array(features)
    
    def train_anomaly_model(self, network_data: List[Dict]):
        """Entraîne le modèle de détection d'anomalies"""
        try:
            all_features = []
            for device_data in network_data:
                features = self.extract_anomaly_features(device_data.get('history', []))
                if len(features) > 0:
                    all_features.extend(features)
            
            if len(all_features) > 10:
                features_array = np.array(all_features)
                features_scaled = self.scaler.fit_transform(features_array)
                self.isolation_forest.fit(features_scaled)
                self.is_fitted = True
                logger.info("Modèle d'anomalies entraîné avec succès")
            else:
                logger.warning("Données insuffisantes pour entraîner le modèle d'anomalies")
        except Exception as e:
            logger.error(f"Erreur entraînement modèle anomalies: {e}")
    
    def detect_anomalies(self, device_history: List[Dict]) -> Dict:
        """Détecte les anomalies pour un équipement"""
        try:
            if not self.is_fitted or not device_history:
                return {'is_anomaly': False, 'anomaly_score': 0.0, 'confidence': 0.0}
            
            features = self.extract_anomaly_features(device_history)
            if len(features) == 0:
                return {'is_anomaly': False, 'anomaly_score': 0.0, 'confidence': 0.0}
            
            features_scaled = self.scaler.transform(features)
            anomaly_scores = self.isolation_forest.decision_function(features_scaled)
            predictions = self.isolation_forest.predict(features_scaled)
            
            # Calcul du score d'anomalie moyen
            avg_anomaly_score = np.mean(anomaly_scores)
            is_anomaly = np.any(predictions == -1)
            
            return {
                'is_anomaly': bool(is_anomaly),
                'anomaly_score': float(avg_anomaly_score),
                'confidence': abs(avg_anomaly_score),
                'recent_anomalies': int(np.sum(predictions == -1))
            }
        except Exception as e:
            logger.error(f"Erreur détection anomalies: {e}")
            return {'is_anomaly': False, 'anomaly_score': 0.0, 'confidence': 0.0}

class PredictiveMaintenance:
    """Prédiction de maintenance préventive"""
    
    def __init__(self):
        self.failure_predictor = RandomForestClassifier(n_estimators=100, random_state=42)
        self.uptime_predictor = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_fitted = False
        
    def extract_maintenance_features(self, device_history: List[Dict]) -> np.ndarray:
        """Extrait les caractéristiques pour la prédiction de maintenance"""
        if not device_history:
            return np.array([])
        
        # Calcul des métriques sur les 30 derniers jours
        recent_history = device_history[-30:] if len(device_history) >= 30 else device_history
        
        features = []
        
        # Métriques de disponibilité
        uptime_ratio = sum(1 for h in recent_history if h.get('is_online', False)) / len(recent_history)
        
        # Métriques de performance
        response_times = [h.get('response_time', 0) for h in recent_history if h.get('response_time', 0) > 0]
        avg_response_time = np.mean(response_times) if response_times else 0
        max_response_time = np.max(response_times) if response_times else 0
        
        # Métriques d'erreurs
        error_count = sum(1 for h in recent_history if not h.get('is_online', False))
        error_ratio = error_count / len(recent_history)
        
        # Métriques de stabilité
        consecutive_errors = 0
        max_consecutive_errors = 0
        for h in recent_history:
            if not h.get('is_online', False):
                consecutive_errors += 1
                max_consecutive_errors = max(max_consecutive_errors, consecutive_errors)
            else:
                consecutive_errors = 0
        
        # Âge de l'équipement (simulé)
        device_age_days = len(device_history)
        
        features = [
            uptime_ratio,
            avg_response_time,
            max_response_time,
            error_ratio,
            max_consecutive_errors,
            device_age_days,
            len(recent_history)
        ]
        
        return np.array(features)
    
    def train_maintenance_model(self, network_data: List[Dict]):
        """Entraîne le modèle de prédiction de maintenance"""
        try:
            features_list = []
            labels = []
            
            for device_data in network_data:
                features = self.extract_maintenance_features(device_data.get('history', []))
                if len(features) > 0:
                    features_list.append(features)
                    
                    # Label basé sur l'historique récent
                    recent_history = device_data.get('history', [])[-7:]  # 7 derniers jours
                    failure_label = 1 if any(not h.get('is_online', False) for h in recent_history) else 0
                    labels.append(failure_label)
            
            if len(features_list) > 5:
                X = np.array(features_list)
                y = np.array(labels)
                
                X_scaled = self.scaler.fit_transform(X)
                
                # Entraînement du modèle de prédiction de pannes
                self.failure_predictor.fit(X_scaled, y)
                
                # Entraînement du modèle de prédiction d'uptime
                uptime_labels = [1 - label for label in labels]  # Inverser pour l'uptime
                self.uptime_predictor.fit(X_scaled, uptime_labels)
                
                self.is_fitted = True
                logger.info("Modèle de maintenance prédictive entraîné avec succès")
            else:
                logger.warning("Données insuffisantes pour entraîner le modèle de maintenance")
        except Exception as e:
            logger.error(f"Erreur entraînement modèle maintenance: {e}")
    
    def predict_maintenance(self, device_history: List[Dict]) -> Dict:
        """Prédit les besoins de maintenance"""
        try:
            if not self.is_fitted or not device_history:
                return {
                    'failure_probability': 0.0,
                    'uptime_prediction': 1.0,
                    'maintenance_urgency': 'low',
                    'confidence': 0.0
                }
            
            features = self.extract_maintenance_features(device_history)
            if len(features) == 0:
                return {
                    'failure_probability': 0.0,
                    'uptime_prediction': 1.0,
                    'maintenance_urgency': 'low',
                    'confidence': 0.0
                }
            
            features_scaled = self.scaler.transform(features.reshape(1, -1))
            
            # Prédiction de panne
            failure_prob = self.failure_predictor.predict_proba(features_scaled)[0][1]
            
            # Prédiction d'uptime
            uptime_pred = self.uptime_predictor.predict(features_scaled)[0]
            
            # Détermination de l'urgence
            if failure_prob > 0.8:
                urgency = 'critical'
            elif failure_prob > 0.6:
                urgency = 'high'
            elif failure_prob > 0.4:
                urgency = 'medium'
            else:
                urgency = 'low'
            
            return {
                'failure_probability': float(failure_prob),
                'uptime_prediction': float(uptime_pred),
                'maintenance_urgency': urgency,
                'confidence': min(failure_prob + uptime_pred, 1.0)
            }
        except Exception as e:
            logger.error(f"Erreur prédiction maintenance: {e}")
            return {
                'failure_probability': 0.0,
                'uptime_prediction': 1.0,
                'maintenance_urgency': 'low',
                'confidence': 0.0
            }

class SmartRecommendations:
    """Système de recommandations intelligentes"""
    
    def __init__(self):
        self.recommendation_rules = {
            'critical_failure': {
                'threshold': 0.8,
                'message': '🚨 MAINTENANCE CRITIQUE - Intervention immédiate requise',
                'priority': 'critical',
                'actions': ['Maintenance préventive', 'Vérification complète', 'Remplacement si nécessaire']
            },
            'high_failure': {
                'threshold': 0.6,
                'message': '⚠️ RISQUE ÉLEVÉ - Maintenance préventive recommandée',
                'priority': 'high',
                'actions': ['Maintenance préventive', 'Monitoring renforcé']
            },
            'medium_failure': {
                'threshold': 0.4,
                'message': '🟡 SURVEILLANCE - Vérification recommandée',
                'priority': 'medium',
                'actions': ['Vérification périodique', 'Monitoring standard']
            },
            'anomaly_detected': {
                'threshold': -0.5,
                'message': '🔍 COMPORTEMENT ANORMAL - Investigation nécessaire',
                'priority': 'high',
                'actions': ['Analyse des logs', 'Vérification réseau', 'Diagnostic approfondi']
            },
            'performance_degradation': {
                'threshold': 0.3,
                'message': '📉 DÉGRADATION PERFORMANCE - Optimisation recommandée',
                'priority': 'medium',
                'actions': ['Optimisation réseau', 'Mise à jour firmware', 'Nettoyage système']
            }
        }
    
    def generate_recommendations(self, device_data: Dict) -> List[Dict]:
        """Génère des recommandations intelligentes"""
        recommendations = []
        
        # Analyse des données de maintenance
        maintenance_data = device_data.get('maintenance_analysis', {})
        failure_prob = maintenance_data.get('failure_probability', 0.0)
        uptime_pred = maintenance_data.get('uptime_prediction', 1.0)
        
        # Analyse des anomalies
        anomaly_data = device_data.get('anomaly_analysis', {})
        anomaly_score = anomaly_data.get('anomaly_score', 0.0)
        
        # Recommandations basées sur la probabilité de panne
        if failure_prob > self.recommendation_rules['critical_failure']['threshold']:
            recommendations.append({
                'type': 'critical_failure',
                'message': self.recommendation_rules['critical_failure']['message'],
                'priority': self.recommendation_rules['critical_failure']['priority'],
                'actions': self.recommendation_rules['critical_failure']['actions'],
                'confidence': failure_prob
            })
        elif failure_prob > self.recommendation_rules['high_failure']['threshold']:
            recommendations.append({
                'type': 'high_failure',
                'message': self.recommendation_rules['high_failure']['message'],
                'priority': self.recommendation_rules['high_failure']['priority'],
                'actions': self.recommendation_rules['high_failure']['actions'],
                'confidence': failure_prob
            })
        elif failure_prob > self.recommendation_rules['medium_failure']['threshold']:
            recommendations.append({
                'type': 'medium_failure',
                'message': self.recommendation_rules['medium_failure']['message'],
                'priority': self.recommendation_rules['medium_failure']['priority'],
                'actions': self.recommendation_rules['medium_failure']['actions'],
                'confidence': failure_prob
            })
        
        # Recommandations basées sur les anomalies
        if anomaly_score < self.recommendation_rules['anomaly_detected']['threshold']:
            recommendations.append({
                'type': 'anomaly_detected',
                'message': self.recommendation_rules['anomaly_detected']['message'],
                'priority': self.recommendation_rules['anomaly_detected']['priority'],
                'actions': self.recommendation_rules['anomaly_detected']['actions'],
                'confidence': abs(anomaly_score)
            })
        
        # Recommandations basées sur la performance
        if uptime_pred < 0.7:
            recommendations.append({
                'type': 'performance_degradation',
                'message': self.recommendation_rules['performance_degradation']['message'],
                'priority': self.recommendation_rules['performance_degradation']['priority'],
                'actions': self.recommendation_rules['performance_degradation']['actions'],
                'confidence': 1.0 - uptime_pred
            })
        
        # Recommandations spécifiques par type d'équipement
        device_type = device_data.get('device_type', 'unknown')
        if device_type == 'server':
            if failure_prob > 0.5:
                recommendations.append({
                    'type': 'server_maintenance',
                    'message': '🖥️ MAINTENANCE SERVEUR - Vérification système recommandée',
                    'priority': 'high',
                    'actions': ['Vérification disques', 'Analyse logs système', 'Mise à jour sécurité'],
                    'confidence': failure_prob
                })
        elif device_type == 'plc':
            if failure_prob > 0.4:
                recommendations.append({
                    'type': 'plc_maintenance',
                    'message': '⚙️ MAINTENANCE PLC - Vérification automation recommandée',
                    'priority': 'high',
                    'actions': ['Vérification programmes', 'Test sécurité', 'Backup configuration'],
                    'confidence': failure_prob
                })
        
        return recommendations

class AIEnhancement:
    """Module principal d'Intelligence Artificielle"""
    
    def __init__(self):
        self.device_classifier = DeviceClassifier()
        self.anomaly_detector = AnomalyDetector()
        self.maintenance_predictor = PredictiveMaintenance()
        self.recommendation_system = SmartRecommendations()
        self.models_trained = False
        
    def train_all_models(self, network_data: List[Dict]):
        """Entraîne tous les modèles IA"""
        try:
            logger.info("Début de l'entraînement des modèles IA...")
            
            # Entraînement du modèle d'anomalies
            self.anomaly_detector.train_anomaly_model(network_data)
            
            # Entraînement du modèle de maintenance
            self.maintenance_predictor.train_maintenance_model(network_data)
            
            self.models_trained = True
            logger.info("Tous les modèles IA ont été entraînés avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'entraînement des modèles: {e}")
    
    def analyze_device_complete(self, device_data: Dict) -> Dict:
        """Analyse complète d'un équipement avec IA"""
        try:
            # Classification de l'équipement
            classification = self.device_classifier.classify_device(
                device_data.get('hostname', ''),
                device_data.get('mac_vendor', ''),
                device_data.get('ip', '')
            )
            
            # Analyse des anomalies
            anomaly_analysis = self.anomaly_detector.detect_anomalies(
                device_data.get('history', [])
            )
            
            # Analyse de maintenance prédictive
            maintenance_analysis = self.maintenance_predictor.predict_maintenance(
                device_data.get('history', [])
            )
            
            # Génération des recommandations
            device_analysis_data = {
                'device_type': classification['device_type'],
                'maintenance_analysis': maintenance_analysis,
                'anomaly_analysis': anomaly_analysis
            }
            
            recommendations = self.recommendation_system.generate_recommendations(
                device_analysis_data
            )
            
            # Calcul du score de santé global
            health_score = self.calculate_health_score(
                maintenance_analysis, anomaly_analysis, classification
            )
            
            return {
                'classification': classification,
                'anomaly_analysis': anomaly_analysis,
                'maintenance_analysis': maintenance_analysis,
                'recommendations': recommendations,
                'health_score': health_score,
                'analysis_timestamp': datetime.now().isoformat(),
                'ai_confidence': self.calculate_ai_confidence(
                    classification, anomaly_analysis, maintenance_analysis
                )
            }
            
        except Exception as e:
            logger.error(f"Erreur analyse IA complète: {e}")
            return {
                'classification': {'device_type': 'unknown', 'confidence': 0.0},
                'anomaly_analysis': {'is_anomaly': False, 'anomaly_score': 0.0},
                'maintenance_analysis': {'failure_probability': 0.0, 'maintenance_urgency': 'low'},
                'recommendations': [],
                'health_score': 0.0,
                'analysis_timestamp': datetime.now().isoformat(),
                'ai_confidence': 0.0
            }
    
    def calculate_health_score(self, maintenance: Dict, anomaly: Dict, classification: Dict) -> float:
        """Calcule un score de santé global"""
        try:
            # Score de maintenance (0-100)
            maintenance_score = (1 - maintenance.get('failure_probability', 0.0)) * 100
            
            # Score d'anomalie (0-100)
            anomaly_score = max(0, (1 + anomaly.get('anomaly_score', 0.0)) * 50)
            
            # Score de classification (0-100)
            classification_score = classification.get('confidence', 0.0) * 100
            
            # Score global pondéré
            health_score = (
                maintenance_score * 0.5 +
                anomaly_score * 0.3 +
                classification_score * 0.2
            )
            
            return max(0, min(100, health_score))
            
        except Exception as e:
            logger.error(f"Erreur calcul score santé: {e}")
            return 50.0
    
    def calculate_ai_confidence(self, classification: Dict, anomaly: Dict, maintenance: Dict) -> float:
        """Calcule la confiance globale de l'IA"""
        try:
            confidences = [
                classification.get('confidence', 0.0),
                anomaly.get('confidence', 0.0),
                maintenance.get('confidence', 0.0)
            ]
            
            return np.mean(confidences)
            
        except Exception as e:
            logger.error(f"Erreur calcul confiance IA: {e}")
            return 0.0
    
    def save_models(self, filepath: str):
        """Sauvegarde les modèles IA"""
        try:
            models_data = {
                'anomaly_detector': {
                    'isolation_forest': self.anomaly_detector.isolation_forest,
                    'scaler': self.anomaly_detector.scaler,
                    'is_fitted': self.anomaly_detector.is_fitted
                },
                'maintenance_predictor': {
                    'failure_predictor': self.maintenance_predictor.failure_predictor,
                    'uptime_predictor': self.maintenance_predictor.uptime_predictor,
                    'scaler': self.maintenance_predictor.scaler,
                    'is_fitted': self.maintenance_predictor.is_fitted
                },
                'models_trained': self.models_trained,
                'timestamp': datetime.now().isoformat()
            }
            
            joblib.dump(models_data, filepath)
            logger.info(f"Modèles IA sauvegardés: {filepath}")
            
        except Exception as e:
            logger.error(f"Erreur sauvegarde modèles: {e}")
    
    def load_models(self, filepath: str):
        """Charge les modèles IA"""
        try:
            models_data = joblib.load(filepath)
            
            # Restauration du détecteur d'anomalies
            self.anomaly_detector.isolation_forest = models_data['anomaly_detector']['isolation_forest']
            self.anomaly_detector.scaler = models_data['anomaly_detector']['scaler']
            self.anomaly_detector.is_fitted = models_data['anomaly_detector']['is_fitted']
            
            # Restauration du prédicteur de maintenance
            self.maintenance_predictor.failure_predictor = models_data['maintenance_predictor']['failure_predictor']
            self.maintenance_predictor.uptime_predictor = models_data['maintenance_predictor']['uptime_predictor']
            self.maintenance_predictor.scaler = models_data['maintenance_predictor']['scaler']
            self.maintenance_predictor.is_fitted = models_data['maintenance_predictor']['is_fitted']
            
            self.models_trained = models_data.get('models_trained', False)
            logger.info(f"Modèles IA chargés: {filepath}")
            
        except Exception as e:
            logger.error(f"Erreur chargement modèles: {e}")

# Instance globale du système IA
ai_system = AIEnhancement() 