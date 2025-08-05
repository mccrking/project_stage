#!/usr/bin/env python3
"""
Module d'intégration DeepSeek API pour le chatbot intelligent
"""

import os
import json
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DeepSeekChatbot:
    """Chatbot intelligent utilisant l'API DeepSeek"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialise le chatbot DeepSeek
        
        Args:
            api_key: Clé API DeepSeek (peut être dans les variables d'environnement)
        """
        self.api_key = api_key or os.getenv('DEEPSEEK_API_KEY')
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.model = "deepseek-chat"
        self.max_tokens = 1000
        self.temperature = 0.7
        
        # Contexte système pour le chatbot
        self.system_prompt = """Tu es un assistant IA spécialisé dans la supervision réseau pour Central Danone. 
Tu as accès aux données en temps réel du réseau et tu peux aider les techniciens avec :

1. **Analyse de la santé réseau** : Score de santé, équipements en ligne/hors ligne
2. **Détection de problèmes** : Alertes actives, équipements critiques
3. **Optimisations** : Recommandations d'amélioration basées sur les données
4. **Sécurité** : Menaces détectées, niveau de sécurité
5. **Performance** : Analyse des performances réseau
6. **Maintenance** : Conseils de maintenance prédictive

Tu dois toujours :
- Répondre en français
- Être précis et professionnel
- Utiliser les données fournies pour tes réponses
- Donner des conseils pratiques et actionnables
- Être concis mais informatif

Format de réponse : Sois direct, utilise des emojis appropriés, et donne des informations chiffrées quand possible."""

    def is_configured(self) -> bool:
        """Vérifie si l'API est configurée"""
        return bool(self.api_key)
    
    def get_network_context(self, devices: List[Dict], alerts: List[Dict]) -> str:
        """
        Génère le contexte réseau pour l'IA
        
        Args:
            devices: Liste des équipements
            alerts: Liste des alertes actives
            
        Returns:
            Contexte formaté pour l'IA
        """
        if not devices:
            return "Aucun équipement surveillé actuellement."
        
        # Statistiques des équipements
        total_devices = len(devices)
        online_devices = sum(1 for d in devices if d.get('is_online', False))
        offline_devices = total_devices - online_devices
        avg_health = sum(d.get('health_score', 0) for d in devices) / total_devices if devices else 0
        critical_devices = sum(1 for d in devices if d.get('maintenance_urgency') == 'critical')
        
        # Alertes actives
        active_alerts = len([a for a in alerts if not a.get('is_resolved', True)])
        
        context = f"""
CONTEXTE RÉSEAU ACTUEL (Données en temps réel) :

📊 ÉQUIPEMENTS :
- Total surveillés : {total_devices}
- En ligne : {online_devices}
- Hors ligne : {offline_devices}
- Score de santé moyen : {avg_health:.1f}%
- Équipements critiques : {critical_devices}

🚨 ALERTES :
- Alertes actives : {active_alerts}

📋 DÉTAILS ÉQUIPEMENTS :
"""
        
        # Ajouter les détails des équipements critiques
        critical_list = [d for d in devices if d.get('maintenance_urgency') == 'critical']
        if critical_list:
            context += "\nÉQUIPEMENTS CRITIQUES :\n"
            for device in critical_list[:5]:  # Limiter à 5
                context += f"- {device.get('hostname', 'Unknown')} ({device.get('ip', 'N/A')}) - Santé: {device.get('health_score', 0):.1f}%\n"
        
        # Ajouter les alertes récentes
        if alerts:
            context += "\nALERTES RÉCENTES :\n"
            for alert in alerts[:3]:  # Limiter à 3
                context += f"- {alert.get('message', 'N/A')}\n"
        
        return context
    
    def chat(self, message: str, devices: List[Dict] = None, alerts: List[Dict] = None) -> Dict[str, Any]:
        """
        Envoie un message au chatbot DeepSeek
        
        Args:
            message: Message de l'utilisateur
            devices: Données des équipements (optionnel)
            alerts: Données des alertes (optionnel)
            
        Returns:
            Réponse du chatbot
        """
        if not self.is_configured():
            return {
                'success': False,
                'error': 'API DeepSeek non configurée. Veuillez définir DEEPSEEK_API_KEY.',
                'fallback': True
            }
        
        try:
            # Préparer le contexte réseau
            network_context = self.get_network_context(devices or [], alerts or [])
            
            # Construire le message complet
            full_message = f"{network_context}\n\nQuestion utilisateur : {message}"
            
            # Préparer la requête API
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': self.model,
                'messages': [
                    {'role': 'system', 'content': self.system_prompt},
                    {'role': 'user', 'content': full_message}
                ],
                'max_tokens': self.max_tokens,
                'temperature': self.temperature,
                'stream': False
            }
            
            # Appel API
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                
                return {
                    'success': True,
                    'response': ai_response,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'confidence': 0.95,
                    'model': self.model,
                    'tokens_used': result.get('usage', {}).get('total_tokens', 0)
                }
            else:
                error_msg = f"Erreur API DeepSeek: {response.status_code} - {response.text}"
                logger.error(error_msg)
                return {
                    'success': False,
                    'error': error_msg,
                    'fallback': True
                }
                
        except requests.exceptions.Timeout:
            error_msg = "Timeout de l'API DeepSeek"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'fallback': True
            }
        except requests.exceptions.RequestException as e:
            error_msg = f"Erreur de connexion DeepSeek: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'fallback': True
            }
        except Exception as e:
            error_msg = f"Erreur inattendue: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'fallback': True
            }
    
    def test_connection(self) -> Dict[str, Any]:
        """Teste la connexion à l'API DeepSeek"""
        if not self.is_configured():
            return {
                'success': False,
                'error': 'API non configurée'
            }
        
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': self.model,
                'messages': [
                    {'role': 'user', 'content': 'Test de connexion'}
                ],
                'max_tokens': 10
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': 'Connexion DeepSeek réussie'
                }
            else:
                return {
                    'success': False,
                    'error': f'Erreur {response.status_code}: {response.text}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Erreur de connexion: {str(e)}'
            }

# Instance globale
deepseek_bot = DeepSeekChatbot() 