import os
import platform

def ping(host):
    # Utilise le chemin complet sous Windows
    if platform.system().lower() == 'windows':
        ping_cmd = r'C:\Windows\System32\ping.exe'
        param = '-n'
    else:
        ping_cmd = 'ping'
        param = '-c'
    command = [ping_cmd, param, '1', host]
    return os.system(' '.join(command)) == 0

if __name__ == '__main__':
    print('Test ping sur 192.168.1.1 (ta box) :')
    if ping('192.168.1.1'):
        print('✅ Réponse reçue ! Le ping fonctionne sur le réseau.')
    else:
        print('❌ Aucun ping reçu. Le fallback du projet ne verra rien si les appareils ne répondent pas au ping.')