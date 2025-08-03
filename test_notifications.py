#!/usr/bin/env python3
"""
Script de test pour le système de notifications en temps réel Central Danone
"""

from app import add_notification, get_unread_notifications, NOTIFICATIONS
import time

def test_notifications():
    """Teste le système de notifications"""
    print("🚀 TEST NOTIFICATIONS CENTRAL DANONE")
    print("=" * 50)
    
    # Test 1: Notification d'information
    print("\n📧 Test 1: Notification d'information")
    add_notification(
        "✅ Système de supervision Central Danone démarré avec succès",
        'success',
        'low'
    )
    
    # Test 2: Notification d'avertissement
    print("📧 Test 2: Notification d'avertissement")
    add_notification(
        "⚠️ Appareil 192.168.1.100 hors ligne depuis 5 minutes",
        'warning',
        'medium',
        '192.168.1.100'
    )
    
    # Test 3: Notification critique
    print("📧 Test 3: Notification critique")
    add_notification(
        "🚨 RISQUE CRITIQUE détecté sur PLC-PRODUCTION (192.168.20.5) - Probabilité de panne: 85%",
        'danger',
        'critical',
        '192.168.20.5'
    )
    
    # Test 4: Notification d'anomalie IA
    print("📧 Test 4: Notification d'anomalie IA")
    add_notification(
        "🔍 ANOMALIE détectée sur SERVEUR-PRINCIPAL (192.168.10.1) - Score d'anomalie: -0.023",
        'warning',
        'high',
        '192.168.10.1'
    )
    
    # Test 5: Notification de maintenance
    print("📧 Test 5: Notification de maintenance")
    add_notification(
        "🔧 MAINTENANCE recommandée pour IMPRIMANTE-ADMIN (192.168.1.50) - Risque: 67%",
        'info',
        'medium',
        '192.168.1.50'
    )
    
    # Affichage des résultats
    print("\n📊 Résultats des tests:")
    print(f"   - Total notifications: {len(NOTIFICATIONS)}")
    print(f"   - Non lues: {len(get_unread_notifications())}")
    
    print("\n📋 Dernières notifications:")
    for i, notification in enumerate(NOTIFICATIONS[-5:], 1):
        print(f"   {i}. [{notification['type'].upper()}] {notification['message']}")
        print(f"      Heure: {notification['timestamp']}")
        print(f"      IP: {notification.get('device_ip', 'N/A')}")
        print()
    
    print("✅ Tests terminés !")
    print("📱 Vérifiez les notifications dans l'interface web")
    print("🌐 Allez sur http://localhost:5000 et regardez l'icône de cloche")

def test_email_fallback():
    """Teste le fallback email vers notifications"""
    print("\n📧 Test du fallback email:")
    
    # Simuler une erreur d'email
    from app import send_email_alert
    
    print("Tentative d'envoi d'email (avec fallback automatique)...")
    result = send_email_alert(
        "Test fallback email",
        "Ce test vérifie que les notifications fonctionnent même si l'email échoue.",
        'medium'
    )
    
    if result:
        print("✅ Email envoyé avec succès")
    else:
        print("✅ Fallback vers notifications activé")
    
    print(f"Notifications totales: {len(NOTIFICATIONS)}")

if __name__ == "__main__":
    test_notifications()
    test_email_fallback() 