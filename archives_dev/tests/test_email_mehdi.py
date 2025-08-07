#!/usr/bin/env python3
"""
Script de test pour configurer l'email de Mehdi et envoyer une alerte de test
"""

from app import EMAIL_CONFIG, send_email_alert, test_email_configuration
import json

def configure_email_for_mehdi():
    """Configure l'email pour Mehdi"""
    print("🔧 Configuration de l'email pour mehdi.chmiti2000@gmail.com...")
    
    # Configuration Gmail pour Mehdi
    EMAIL_CONFIG['enabled'] = True
    EMAIL_CONFIG['smtp_server'] = 'smtp.gmail.com'
    EMAIL_CONFIG['smtp_port'] = 587
    EMAIL_CONFIG['username'] = 'mehdi.chmiti2000@gmail.com'  # À remplacer par votre email d'envoi
    EMAIL_CONFIG['password'] = ''  # À remplacer par votre mot de passe d'application
    EMAIL_CONFIG['from_email'] = 'mehdi.chmiti2000@gmail.com'  # À remplacer par votre email d'envoi
    EMAIL_CONFIG['to_email'] = 'mehdi.chmiti2000@gmail.com'
    
    print("✅ Configuration email mise à jour:")
    print(f"   - Serveur: {EMAIL_CONFIG['smtp_server']}")
    print(f"   - Port: {EMAIL_CONFIG['smtp_port']}")
    print(f"   - Email de destination: {EMAIL_CONFIG['to_email']}")
    print(f"   - Activé: {EMAIL_CONFIG['enabled']}")
    
    return EMAIL_CONFIG

def test_email_send():
    """Teste l'envoi d'email"""
    print("\n📧 Test d'envoi d'email...")
    
    # Test de configuration
    result = test_email_configuration()
    print(f"Résultat du test: {result}")
    
    if result['status'] == 'success':
        print("✅ Configuration email valide !")
        
        # Envoi d'une alerte de test
        print("\n🚨 Envoi d'une alerte de test...")
        success = send_email_alert(
            "Test Central Danone - Mehdi",
            """Ceci est un test d'alerte pour vérifier que votre email mehdi.chmiti2000@gmail.com fonctionne correctement.

Détails du test:
- Système: Central Danone Supervision
- Type: Test de configuration email
- Priorité: Medium
- Heure: Test automatique

Si vous recevez cet email, la configuration est correcte ! 🎉""",
            'medium'
        )
        
        if success:
            print("✅ Alerte de test envoyée avec succès !")
            print("📬 Vérifiez votre boîte mail mehdi.chmiti2000@gmail.com")
        else:
            print("❌ Erreur lors de l'envoi de l'alerte de test")
    else:
        print(f"❌ Erreur de configuration: {result['message']}")
        print("\n💡 Pour configurer Gmail:")
        print("1. Activez l'authentification à 2 facteurs")
        print("2. Générez un mot de passe d'application")
        print("3. Remplacez 'password' dans le script")

def main():
    """Fonction principale"""
    print("=" * 60)
    print("🚀 TEST EMAIL CENTRAL DANONE - MEHDI")
    print("=" * 60)
    
    # Configuration
    configure_email_for_mehdi()
    
    # Test
    test_email_send()
    
    print("\n" + "=" * 60)
    print("✅ Test terminé !")
    print("=" * 60)

if __name__ == "__main__":
    main() 