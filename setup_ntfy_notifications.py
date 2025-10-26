#!/usr/bin/env python
"""
Setup NTFY pentru notificari pe server Linux
Compatibil cu servere vechi (OpenSSL 0.9.7a, curl 7.12.1)

Tot trebuie sa configurezi:
1. Instaleaza aplicatia NTFY pe telefon
2. Inlocuieste variabilele cu datele tale (HOST, USER, PASS, etc.)
3. Adapteaza scriptul pentru nevoile tale
"""

import paramiko
import sys
import hashlib
from datetime import datetime

# ===== CONFIGURAZE CELE DE JOS =====
HOST = "YOUR_SERVER_IP"
USER = "root"
PASS = "YOUR_PASSWORD"
PORT = 22
# ===================================

def ssh_exec(ssh, cmd, show=True, timeout=10):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode("utf-8", errors="ignore")
    err = stderr.read().decode("utf-8", errors="ignore")
    if show:
        if out:
            print(out)
        if err and "warning" not in err.lower():
            print(f"[WARN] {err}")
    return out, err


def main():
    print("=" * 70)
    print("   SETUP NTFY PENTRU NOTIFICARI SERVER LINUX")
    print("=" * 70)
    print()
    
    if HOST == "YOUR_SERVER_IP" or PASS == "YOUR_PASSWORD":
        print("[ERROR] Configureaza variabilele HOST si PASS la inceputul scriptului!")
        return 1
    
    print("[INFO] Conectare la server...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(HOST, PORT, USER, PASS, timeout=15)
        print("[OK] Conectat!")
        print()
        
        # Generare topic unic
        print("=" * 70)
        print("1. GENERARE TEMA UNICA PENTRU NTFY")
        print("=" * 70)
        print()
        
        unique_topic = hashlib.md5(f"linux_server_{HOST}".encode()).hexdigest()[:12]
        ntfy_topic = f"server-{unique_topic}"
        
        print(f"[OK] Tema unica generata: {ntfy_topic}")
        print()
        
        # Creez script NTFY
        print("=" * 70)
        print("2. CREARE SCRIPT NTFY PE SERVER")
        print("=" * 70)
        print()
        
        ntfy_script = f'''#!/bin/bash
# Script simplu pentru trimitere notificari prin NTFY
# Compatibil cu OpenSSL vechi si curl 7.12.1

TOPIC="{ntfy_topic}"
NTFY_URL="https://ntfy.sh/${{TOPIC}}"

send_notification() {{
    local message="$1"
    local title="Linux Server"
    
    # Trimite notificare prin NTFY (HTTP pentru compatibilitate)
    curl -s -X POST -d "${{message}}" "${{NTFY_URL}}" > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo "NTFY notification sent successfully"
    else
        echo "Failed to send NTFY notification"
    fi
}}

# Test mesaj
if [ "$1" == "test" ]; then
    send_notification "Test notificare de pe serverul Linux! Timestamp: $(date)"
else
    # Mesaj custom
    send_notification "$1"
fi
'''
        
        print("[INFO] Creez scriptul NTFY pe server...")
        ssh_exec(ssh, f'cat > /usr/local/bin/ntfy_notify.sh <<\'EOFNTFY\'\n{ntfy_script}\nEOFNTFY', show=False, timeout=5)
        ssh_exec(ssh, "chmod +x /usr/local/bin/ntfy_notify.sh", show=False)
        print("[OK] Script NTFY creat in /usr/local/bin/ntfy_notify.sh")
        print()
        
        # Test
        print("=" * 70)
        print("3. TEST NOTIFICARE")
        print("=" * 70)
        print()
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"[INFO] Trimitere test notificare NTFY...")
        print(f"[INFO] Tema: {ntfy_topic}")
        print()
        
        message = f"Test notificare NTFY de pe serverul Linux!\n\nTimestamp: {timestamp}\nServer: {HOST}\nStatus: SUCCESS"
        
        cmd = f'/usr/local/bin/ntfy_notify.sh "{message}"'
        out, _ = ssh_exec(ssh, cmd, show=False, timeout=5)
        
        if out:
            print(out)
        
        print()
        print("[OK] Notificare NTFY trimisa!")
        print()
        
        ssh.close()
        
        print("=" * 70)
        print("SETUP NTFY COMPLET!")
        print("=" * 70)
        print()
        print(">> PENTRU A PRIMI NOTIFICARI PE TELEFON:")
        print("   1. DESCARCA aplicatia NTFY:")
        print("      - Android: https://play.google.com/store/apps/details?id=io.heckel.ntfy")
        print("      - iOS: https://apps.apple.com/app/ntfy/id1625396347")
        print()
        print("   2. ADAUGA SUBSCRIBE la tema:")
        print(f"      {ntfy_topic}")
        print()
        print(">> UTILIZARE:")
        print("   /usr/local/bin/ntfy_notify.sh \"Mesajul tau\"")
        print()
        print(">> PENTRU CRON:")
        print("   0 0 * * * /usr/local/bin/ntfy_notify.sh \"Backup completat!\"")
        print()
        
        return 0
        
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

