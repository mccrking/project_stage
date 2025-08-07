#!/usr/bin/env python3
"""
Mode démo IA - Simule les réponses intelligentes sans API externe
"""

import json
import random
from datetime import datetime

class DemoAIAssistant:
    """Assistant IA en mode démo pour tester l'interface"""
    
    def __init__(self):
        self.demo_responses = {
            'network_analysis': [
                "✅ Réseau stable. 2 équipements détectés, tous fonctionnels.",
                "⚠️ Temps de réponse élevé détecté sur 192.168.0.1 (45ms).",
                "🔍 Analyse terminée. Pas d'anomalie détectée sur le réseau.",
                "📊 Performance réseau optimale. Uptime moyen: 99.5%."
            ],
            'security_check': [
                "🛡️ Aucune menace détectée. Tous les ports critiques sont sécurisés.",
                "⚠️ Port 22 (SSH) ouvert sur plusieurs équipements. Vérifiez l'accès.",
                "✅ Configuration firewall optimale détectée.",
                "🔐 Audit sécurité: 8/10. Recommandations disponibles."
            ],
            'maintenance': [
                "🔧 Maintenance recommandée pour l'équipement 192.168.0.1 (uptime > 30 jours).",
                "✅ Tous les équipements sont à jour.",
                "📅 Planification maintenance: Aucune intervention urgente requise.",
                "⚡ Optimisation possible: Mise à jour firmware disponible."
            ],
            'general': [
                "👋 Bonjour! Je suis l'assistant IA de surveillance réseau Danone.",
                "🤖 Comment puis-je vous aider avec votre infrastructure réseau?",
                "📈 L'analyse de votre réseau est disponible. Que souhaitez-vous examiner?",
                "🎯 Surveillance active. Tout fonctionne correctement!"
            ]
        }
    
    def analyze_query(self, message):
        """Analyse le message et retourne une catégorie"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['réseau', 'network', 'ping', 'connexion']):
            return 'network_analysis'
        elif any(word in message_lower for word in ['sécurité', 'security', 'port', 'firewall']):
            return 'security_check'
        elif any(word in message_lower for word in ['maintenance', 'update', 'firmware', 'uptime']):
            return 'maintenance'
        else:
            return 'general'
    
    def generate_response(self, message, devices_data=None, alerts_data=None):
        """Génère une réponse démo intelligente"""
        
        category = self.analyze_query(message)
        base_response = random.choice(self.demo_responses[category])
        
        # Ajouter des informations contextuelles si disponibles
        context_info = ""
        if devices_data:
            device_count = len(devices_data)
            context_info += f"\n\n📊 Contexte actuel:\n- {device_count} équipements surveillés"
            
            online_devices = [d for d in devices_data if d.get('is_online', True)]
            context_info += f"\n- {len(online_devices)} équipements en ligne"
        
        if alerts_data:
            alert_count = len(alerts_data)
            if alert_count > 0:
                context_info += f"\n- ⚠️ {alert_count} alerte(s) active(s)"
        
        # Ajouter des recommandations spécifiques
        recommendations = self._generate_recommendations(category, devices_data)
        
        full_response = base_response + context_info + recommendations
        
        return {
            'success': True,
            'response': full_response,
            'model': 'Demo AI Assistant',
            'timestamp': datetime.now().isoformat(),
            'category': category
        }
    
    def _generate_recommendations(self, category, devices_data):
        """Génère des recommandations contextuelles"""
        
        recommendations = "\n\n💡 Recommandations:"
        
        if category == 'network_analysis':
            if devices_data and len(devices_data) < 5:
                recommendations += "\n- Envisagez d'étendre la surveillance à plus d'équipements"
            recommendations += "\n- Planifiez des scans réguliers toutes les 15 minutes"
            
        elif category == 'security_check':
            recommendations += "\n- Activez l'authentification 2FA sur les équipements critiques"
            recommendations += "\n- Surveillez les tentatives de connexion échouées"
            
        elif category == 'maintenance':
            recommendations += "\n- Programmez une fenêtre de maintenance hebdomadaire"
            recommendations += "\n- Documentez les interventions pour traçabilité"
            
        else:
            recommendations += "\n- Consultez le tableau de bord pour plus de détails"
            recommendations += "\n- Configurez les notifications email pour les alertes"
        
        return recommendations
    
    def test_connection(self):
        """Simule un test de connexion réussi"""
        return {
            'success': True,
            'message': 'Assistant IA démo opérationnel',
            'model': 'Demo AI Assistant',
            'version': '1.0.0'
        }

# Instance globale pour la compatibilité
demo_ai = DemoAIAssistant()

# Fonction de test
def test_demo_ai():
    """Test de l'assistant démo"""
    print("🤖 Test de l'Assistant IA Démo")
    print("=" * 40)
    
    test_messages = [
        "Comment va le réseau?",
        "Y a-t-il des problèmes de sécurité?",
        "Quand faire la maintenance?",
        "Bonjour, comment ça va?"
    ]
    
    for message in test_messages:
        print(f"\n❓ Question: {message}")
        response = demo_ai.generate_response(message)
        print(f"🤖 Réponse: {response['response']}")
        print(f"🏷️ Catégorie: {response['category']}")
    
    print("\n✅ Test terminé!")

if __name__ == "__main__":
    test_demo_ai()
