#!/usr/bin/env python3
"""
Chatbot Groq pour Central Danone
"""

import requests
import json
import logging
from datetime import datetime
from typing import List, Dict, Any
from config_groq import GroqConfig

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GroqChatbot:
    """Chatbot utilisant l'API Groq"""
    
    def __init__(self):
        """Initialise le chatbot Groq"""
        self.config = GroqConfig()
        self.api_key = self.config.API_KEY
        self.api_url = self.config.API_URL
        self.model = self.config.MODEL
        self.max_tokens = self.config.MAX_TOKENS
        self.temperature = self.config.TEMPERATURE
        self.timeout = self.config.TIMEOUT
        
        # Prompt système pour le contexte réseau
        self.system_prompt = """Tu es un assistant IA spécialisé dans la supervision réseau pour Central Danone. 
Tu analyses les données réseau en temps réel et fournis des recommandations intelligentes.

CONTEXTE :
- Tu surveilles un réseau d'entreprise
- Tu as accès aux données des équipements et alertes
- Tu parles en français
- Tu es professionnel et précis

RÔLE :
- Analyser la santé du réseau
- Détecter les problèmes
- Fournir des recommandations d'optimisation
- Répondre aux questions techniques
- Être proactif dans tes suggestions

STYLE :
- Réponses claires et concises
- Langage professionnel
- Recommandations actionnables
- Analyse basée sur les données fournies"""

    def test_connection(self) -> Dict[str, Any]:
        """Teste la connexion à l'API Groq"""
        try:
            if not self.api_key:
                return {
                    'success': False,
                    'error': 'API Groq non configurée. Veuillez définir GROQ_API_KEY.'
                }
            
            # Test simple avec une question basique
            test_response = self._call_api("Test de connexion")
            
            if test_response['success']:
                return {
                    'success': True,
                    'message': 'Connexion Groq réussie',
                    'model': self.model,
                    'response_time': test_response.get('response_time', 0)
                }
            else:
                return {
                    'success': False,
                    'error': test_response['error']
                }
                
        except Exception as e:
            logger.error(f"Erreur test connexion Groq: {e}")
            return {
                'success': False,
                'error': f"Erreur test connexion: {str(e)}"
            }

    def _generate_network_context(self, devices: List[Dict], alerts: List[Dict]) -> str:
        """Génère le contexte réseau pour l'IA"""
        context = "\n\nDONNÉES RÉSEAU ACTUELLES:\n"
        
        # Statistiques des équipements
        total_devices = len(devices)
        online_devices = sum(1 for d in devices if d.get('is_online', False))
        offline_devices = total_devices - online_devices
        
        context += f"- Équipements surveillés: {total_devices}\n"
        context += f"- En ligne: {online_devices}\n"
        context += f"- Hors ligne: {offline_devices}\n"
        
        # Équipements critiques
        critical_devices = [d for d in devices if d.get('maintenance_urgency') == 'critical']
        if critical_devices:
            context += f"- Équipements critiques: {len(critical_devices)}\n"
            for device in critical_devices[:3]:  # Limiter à 3
                context += f"  * {device.get('hostname', 'N/A')} ({device.get('ip', 'N/A')})\n"
        
        # Alertes actives
        active_alerts = [a for a in alerts if not a.get('is_resolved', True)]
        if active_alerts:
            context += f"- Alertes actives: {len(active_alerts)}\n"
            for alert in active_alerts[:3]:  # Limiter à 3
                context += f"  * {alert.get('message', 'N/A')} (Priorité: {alert.get('priority', 'N/A')})\n"
        
        # Scores de santé moyens
        health_scores = [d.get('health_score', 0) for d in devices if d.get('health_score')]
        if health_scores:
            avg_health = sum(health_scores) / len(health_scores)
            context += f"- Score de santé moyen: {avg_health:.1f}%\n"
        
        return context

    def _call_api(self, message: str, devices: List[Dict] = None, alerts: List[Dict] = None) -> Dict[str, Any]:
        """Appelle l'API Groq"""
        try:
            if not self.api_key:
                return {
                    'success': False,
                    'error': 'API Groq non configurée'
                }
            
            # Préparer le contexte
            context = self.system_prompt
            if devices and alerts:
                context += self._generate_network_context(devices, alerts)
            
            # Préparer les messages
            messages = [
                {"role": "system", "content": context},
                {"role": "user", "content": message}
            ]
            
            # Préparer la requête
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature
            }
            
            # Appel API
            start_time = datetime.now()
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=self.timeout
            )
            response_time = (datetime.now() - start_time).total_seconds()
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                tokens_used = result.get('usage', {}).get('total_tokens', 0)
                
                return {
                    'success': True,
                    'response': content,
                    'confidence': 0.95,  # Groq est très fiable
                    'model': 'Groq',
                    'tokens_used': tokens_used,
                    'response_time': response_time
                }
            else:
                error_msg = f"Erreur {response.status_code}: {response.text}"
                logger.error(f"Erreur API Groq: {error_msg}")
                return {
                    'success': False,
                    'error': error_msg
                }
                
        except requests.exceptions.Timeout:
            error_msg = "Timeout de l'API Groq"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
        except requests.exceptions.RequestException as e:
            error_msg = f"Erreur requête Groq: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
        except Exception as e:
            error_msg = f"Erreur inattendue Groq: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }

    def chat(self, message: str, devices: List[Dict] = None, alerts: List[Dict] = None) -> Dict[str, Any]:
        """Chat avec l'IA Groq"""
        try:
            # Appel API Groq
            result = self._call_api(message, devices, alerts)
            
            if result['success']:
                logger.info(f"Groq réussi: {result['response'][:100]}...")
                return result
            else:
                # Fallback vers le système local
                logger.warning(f"Groq échoué: {result['error']}, utilisation du fallback")
                return self._fallback_response(message, devices, alerts)
                
        except Exception as e:
            logger.error(f"Erreur chat Groq: {e}")
            return self._fallback_response(message, devices, alerts)

    def _fallback_response(self, message: str, devices: List[Dict] = None, alerts: List[Dict] = None) -> Dict[str, Any]:
        """Réponse de fallback si Groq échoue"""
        try:
            # Analyse simple du message
            message_lower = message.lower()
            
            # Réponses contextuelles basées sur les données
            if devices:
                total_devices = len(devices)
                online_devices = sum(1 for d in devices if d.get('is_online', False))
                offline_devices = total_devices - online_devices
                
                if any(word in message_lower for word in ['bonjour', 'salut', 'hello']):
                    response = f"Bonjour ! Je suis l'assistant IA de Central Danone. Je surveille actuellement {total_devices} équipements ({online_devices} en ligne, {offline_devices} hors ligne). Comment puis-je vous aider ?"
                
                elif any(word in message_lower for word in ['réseau', 'état', 'santé']):
                    health_scores = [d.get('health_score', 0) for d in devices if d.get('health_score')]
                    avg_health = sum(health_scores) / len(health_scores) if health_scores else 0
                    response = f"L'état du réseau est stable. {online_devices}/{total_devices} équipements sont en ligne. Score de santé moyen: {avg_health:.1f}%."
                
                elif any(word in message_lower for word in ['problème', 'erreur', 'alerte']):
                    if alerts:
                        active_alerts = [a for a in alerts if not a.get('is_resolved', True)]
                        if active_alerts:
                            response = f"J'ai détecté {len(active_alerts)} alertes actives. Vérifiez les équipements critiques et les alertes prioritaires."
                        else:
                            response = "Aucun problème détecté actuellement. Le réseau fonctionne normalement."
                    else:
                        response = "Aucune alerte active en ce moment."
                
                else:
                    response = f"Je surveille {total_devices} équipements. {online_devices} sont en ligne. Que souhaitez-vous savoir ?"
            else:
                response = "Bonjour ! Je suis l'assistant IA de Central Danone. Comment puis-je vous aider ?"
            
            return {
                'success': True,
                'response': response,
                'confidence': 0.8,
                'model': 'Fallback',
                'tokens_used': 0,
                'response_time': 0.1
            }
            
        except Exception as e:
            logger.error(f"Erreur fallback: {e}")
            return {
                'success': True,
                'response': "Bonjour ! Je suis l'assistant IA de Central Danone. Comment puis-je vous aider ?",
                'confidence': 0.7,
                'model': 'Fallback',
                'tokens_used': 0,
                'response_time': 0.1
            }

# Instance globale
groq_bot = GroqChatbot() 