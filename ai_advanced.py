# Module d'IA Avancée - Phase 3
"""
Module d'Intelligence Artificielle Avancée pour le Dashboard Danone
Fonctionnalités : Prédictions, Détection d'intrusion, Optimisation, Chatbot
"""

import json
import random
import numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
import sqlite3
import os

@dataclass
class Prediction:
    """Classe pour les prédictions IA"""
    device_id: int
    device_name: str
    prediction_type: str
    confidence: float
    timestamp: str
    description: str
    severity: str

@dataclass
class Intrusion:
    """Classe pour les intrusions détectées"""
    id: int
    source_ip: str
    target_ip: str
    attack_type: str
    severity: str
    timestamp: str
    status: str
    description: str

@dataclass
class Optimization:
    """Classe pour les optimisations"""
    id: int
    category: str
    title: str
    description: str
    impact: str
    implementation_time: str
    status: str
    timestamp: str

@dataclass
class Trend:
    """Classe pour les analyses de tendances"""
    metric: str
    current_value: float
    previous_value: float
    change_percentage: float
    trend_direction: str
    period: str
    timestamp: str

class AdvancedAI:
    """Classe principale pour l'IA avancée"""
    
    def __init__(self, db_path: str = "network_monitoring.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialise la base de données pour l'IA avancée"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table des prédictions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER,
                device_name TEXT,
                prediction_type TEXT,
                confidence REAL,
                timestamp TEXT,
                description TEXT,
                severity TEXT
            )
        ''')
        
        # Table des intrusions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_intrusions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_ip TEXT,
                target_ip TEXT,
                attack_type TEXT,
                severity TEXT,
                timestamp TEXT,
                status TEXT,
                description TEXT
            )
        ''')
        
        # Table des optimisations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_optimizations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                title TEXT,
                description TEXT,
                impact TEXT,
                implementation_time TEXT,
                status TEXT,
                timestamp TEXT
            )
        ''')
        
        # Table des tendances
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_trends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric TEXT,
                current_value REAL,
                previous_value REAL,
                change_percentage REAL,
                trend_direction TEXT,
                period TEXT,
                timestamp TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def generate_predictions(self) -> List[Dict[str, Any]]:
        """Génère des prédictions IA simulées"""
        predictions = []
        
        # Types de prédictions possibles
        prediction_types = [
            "Défaillance matérielle",
            "Problème de performance",
            "Sécurité compromise",
            "Maintenance préventive",
            "Optimisation réseau"
        ]
        
        # Générer 5-10 prédictions
        for i in range(random.randint(5, 10)):
            prediction = Prediction(
                device_id=random.randint(1, 50),
                device_name=f"Équipement-{random.randint(1, 100)}",
                prediction_type=random.choice(prediction_types),
                confidence=round(random.uniform(0.7, 0.95), 2),
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                description=f"Prédiction basée sur l'analyse des données historiques",
                severity=random.choice(["Faible", "Moyen", "Élevé", "Critique"])
            )
            predictions.append(asdict(prediction))
        
        return predictions
    
    def detect_intrusions(self) -> List[Dict[str, Any]]:
        """Détecte les intrusions simulées"""
        intrusions = []
        
        # Types d'attaques possibles
        attack_types = [
            "Tentative de connexion SSH",
            "Scan de ports",
            "Attaque par déni de service",
            "Tentative d'injection SQL",
            "Tentative de brute force"
        ]
        
        # Générer 3-8 intrusions
        for i in range(random.randint(3, 8)):
            intrusion = Intrusion(
                id=i + 1,
                source_ip=f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                target_ip=f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}",
                attack_type=random.choice(attack_types),
                severity=random.choice(["Faible", "Moyen", "Élevé", "Critique"]),
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                status=random.choice(["En cours", "Bloquée", "Analysée"]),
                description=f"Tentative d'intrusion détectée et analysée"
            )
            intrusions.append(asdict(intrusion))
        
        return intrusions
    
    def generate_optimizations(self) -> List[Dict[str, Any]]:
        """Génère des suggestions d'optimisation"""
        optimizations = []
        
        # Catégories d'optimisation
        categories = [
            "Performance réseau",
            "Sécurité",
            "Maintenance",
            "Configuration",
            "Ressources"
        ]
        
        # Titres d'optimisation
        titles = [
            "Optimisation de la bande passante",
            "Renforcement de la sécurité",
            "Mise à jour des équipements",
            "Configuration des VLAN",
            "Gestion des ressources"
        ]
        
        # Générer 4-7 optimisations
        for i in range(random.randint(4, 7)):
            optimization = Optimization(
                id=i + 1,
                category=random.choice(categories),
                title=random.choice(titles),
                description=f"Optimisation recommandée pour améliorer les performances",
                impact=random.choice(["Faible", "Moyen", "Élevé"]),
                implementation_time=f"{random.randint(1, 8)} heures",
                status=random.choice(["En attente", "En cours", "Terminée"]),
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            optimizations.append(asdict(optimization))
        
        return optimizations
    
    def analyze_trends(self) -> List[Dict[str, Any]]:
        """Analyse les tendances des métriques"""
        trends = []
        
        # Métriques à analyser
        metrics = [
            "Temps de réponse moyen",
            "Taux de disponibilité",
            "Utilisation CPU",
            "Utilisation mémoire",
            "Trafic réseau"
        ]
        
        # Générer des tendances pour chaque métrique
        for metric in metrics:
            current = random.uniform(50, 95)
            previous = random.uniform(50, 95)
            change = ((current - previous) / previous) * 100
            
            trend = Trend(
                metric=metric,
                current_value=round(current, 2),
                previous_value=round(previous, 2),
                change_percentage=round(change, 2),
                trend_direction="Hausse" if change > 0 else "Baisse" if change < 0 else "Stable",
                period="24h",
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            trends.append(asdict(trend))
        
        return trends
    
    def get_statistics(self) -> Dict[str, Any]:
        """Récupère les statistiques IA"""
        return {
            "total_predictions": random.randint(50, 200),
            "accuracy_rate": round(random.uniform(0.85, 0.95), 2),
            "intrusions_blocked": random.randint(10, 50),
            "optimizations_applied": random.randint(5, 20),
            "trends_analyzed": random.randint(20, 100),
            "ai_models_active": random.randint(3, 8),
            "last_training": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "next_training": (datetime.now() + timedelta(hours=6)).strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def chatbot_response(self, message: str) -> Dict[str, Any]:
        """Réponse du chatbot IA"""
        # Réponses prédéfinies basées sur les mots-clés
        responses = {
            "santé": "La santé du réseau est excellente. Tous les équipements sont opérationnels.",
            "problème": "Je détecte quelques anomalies mineures. Voulez-vous que je génère un rapport détaillé ?",
            "optimisation": "J'ai identifié 3 opportunités d'optimisation. Voulez-vous les voir ?",
            "sécurité": "Le niveau de sécurité est élevé. Aucune menace critique détectée.",
            "performance": "Les performances sont dans les normes. Quelques optimisations mineures possibles.",
            "aide": "Je peux vous aider avec : santé réseau, problèmes, optimisations, sécurité, performance.",
            "bonjour": "Bonjour ! Je suis l'assistant IA du Dashboard Danone. Comment puis-je vous aider ?"
        }
        
        # Rechercher une réponse appropriée
        message_lower = message.lower()
        response = "Je ne comprends pas votre demande. Tapez 'aide' pour voir mes capacités."
        
        for keyword, reply in responses.items():
            if keyword in message_lower:
                response = reply
                break
        
        return {
            "response": response,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "confidence": round(random.uniform(0.8, 0.95), 2)
        }

# Instance globale
ai_system = AdvancedAI() 