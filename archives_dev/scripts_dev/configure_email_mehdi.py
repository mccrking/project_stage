#!/usr/bin/env python3
"""
Script interactif pour configurer l'email de Mehdi avec mot de passe d'application
"""

from app import EMAIL_CONFIG, send_email_alert, test_email_configuration
import getpass

def configure_email_interactive():
    """Configuration interactive de l'email"""
    print("🔧 Configuration Email Central Danone - Mehdi")
    print("=" * 50)
    
    # Demander les informations
    print("\n📧 Configuration Gmail:")
    print("1. Activez l'authentification à 2 facteurs sur votre compte Gmail")
    print("2. Générez un mot de passe d'application")
    print("3. Entrez les informations ci-dessous:")
    
    # Email d'envoi (peut être différent de l'email de réception)
    from_email = input("\nEmail d'envoi (ex: mehdi.chmiti2000@gmail.com): ").strip()
    if not from_email:
        from_email = "mehdi.chmiti2000@gmail.com"
    
    # Mot de passe d'application
    print("\n🔐 Mot de passe d'application Gmail:")
    print("(16 caractères, généré dans les paramètres de sécurité Gmail)")
    password = getpass.getpass("Mot de passe d'application: ").strip()
    
    # Email de destination
    to_email = input("\nEmail de destination (ex: mehdi.chmiti2000@gmail.com): ").strip()
    if not to_email:
        to_email = "mehdi.chmiti2000@gmail.com"
    
    # Configuration
    EMAIL_CONFIG['enabled'] = True
    EMAIL_CONFIG['smtp_server'] = 'smtp.gmail.com'
    EMAIL_CONFIG['smtp_port'] = 587
    EMAIL_CONFIG['username'] = from_email
    EMAIL_CONFIG['password'] = password
    EMAIL_CONFIG['from_email'] = from_email
    EMAIL_CONFIG['to_email'] = to_email
    
    print(f"\n✅ Configuration enregistrée:")
    print(f"   - Serveur: {EMAIL_CONFIG['smtp_server']}")
    print(f"   - Port: {EMAIL_CONFIG['smtp_port']}")
    print(f"   - Email d'envoi: {EMAIL_CONFIG['from_email']}")
    print(f"   - Email de destination: {EMAIL_CONFIG['to_email']}")
    print(f"   - Activé: {EMAIL_CONFIG['enabled']}")
    
    return EMAIL_CONFIG

def test_and_send():
    """Teste et envoie une alerte"""
    print("\n📧 Test de la configuration...")
    
    # Test de configuration
    result = test_email_configuration()
    
    if result['status'] == 'success':
        print("✅ Configuration valide !")
        
        # Demander si on veut envoyer un test
        send_test = input("\n🚨 Envoyer une alerte de test ? (o/n): ").strip().lower()
        
        if send_test in ['o', 'oui', 'y', 'yes']:
            print("\n📤 Envoi de l'alerte de test...")
            success = send_email_alert(
                "Test Central Danone - Configuration Réussie",
                f"""🎉 Félicitations ! Votre configuration email fonctionne parfaitement.

Détails de la configuration:
- Système: Central Danone Supervision
- Email configuré: {EMAIL_CONFIG['to_email']}
- Serveur SMTP: {EMAIL_CONFIG['smtp_server']}
- Statut: ✅ Opérationnel

Vous recevrez maintenant automatiquement:
• Alertes d'appareils hors ligne
• Alertes de risques critiques détectés par IA
• Alertes d'anomalies de comportement
• Rapports quotidiens

Merci d'avoir configuré le système de supervision Central Danone ! 🏭""",
                'medium'
            )
            
            if success:
                print("✅ Alerte de test envoyée avec succès !")
                print(f"📬 Vérifiez votre boîte mail: {EMAIL_CONFIG['to_email']}")
            else:
                print("❌ Erreur lors de l'envoi")
        else:
            print("✅ Configuration testée avec succès !")
    else:
        print(f"❌ Erreur: {result['message']}")
        print("\n💡 Vérifiez:")
        print("1. L'authentification à 2 facteurs est activée")
        print("2. Le mot de passe d'application est correct")
        print("3. L'email d'envoi est valide")

def main():
    """Fonction principale"""
    print("🚀 Configuration Email Central Danone")
    print("=" * 50)
    
    try:
        # Configuration
        configure_email_interactive()
        
        # Test et envoi
        test_and_send()
        
        print("\n" + "=" * 50)
        print("✅ Configuration terminée !")
        print("=" * 50)
        
    except KeyboardInterrupt:
        print("\n\n❌ Configuration annulée par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")

if __name__ == "__main__":
    main() 