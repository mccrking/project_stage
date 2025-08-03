#!/usr/bin/env python3
"""
Serveur de développement avec auto-reload
"""

import os
import sys
import time
import subprocess
import signal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class AppReloader(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.restart_app()
    
    def restart_app(self):
        """Redémarre l'application Flask"""
        if self.process:
            print("🔄 Redémarrage de l'application...")
            self.process.terminate()
            self.process.wait()
        
        print("🚀 Démarrage de l'application...")
        self.process = subprocess.Popen([sys.executable, 'app.py'])
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        # Ignorer les fichiers temporaires
        if event.src_path.endswith('.pyc') or '__pycache__' in event.src_path:
            return
        
        # Ignorer les fichiers de base de données
        if event.src_path.endswith('.db') or event.src_path.endswith('.sqlite'):
            return
        
        print(f"📝 Fichier modifié: {event.src_path}")
        time.sleep(1)  # Attendre que le fichier soit complètement écrit
        self.restart_app()

def main():
    print("🔧 Serveur de développement Central Danone")
    print("📁 Surveillance des modifications de fichiers...")
    print("⏹️  Arrêt: Ctrl+C")
    print("-" * 50)
    
    # Créer l'observateur
    event_handler = AppReloader()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⏹️  Arrêt du serveur de développement...")
        if event_handler.process:
            event_handler.process.terminate()
        observer.stop()
    
    observer.join()

if __name__ == "__main__":
    main() 