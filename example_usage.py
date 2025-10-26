#!/usr/bin/env python
"""
Example usage of NTFY notifications

Acest fisier arata cum sa folosesti notificarile NTFY in diferite scenarii.
"""

import paramiko

# ATENTIE: Inlocuieste cu datele tale!
HOST = "YOUR_SERVER_IP"
USER = "root"
PASS = "YOUR_PASSWORD"
PORT = 22


def send_ntfy_notification(message):
    """Trimite notificare NTFY prin SSH"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(HOST, PORT, USER, PASS, timeout=15)
        
        # Trimite notificare
        stdin, stdout, stderr = ssh.exec_command(
            f'/usr/local/bin/ntfy_notify.sh "{message}"'
        )
        
        result = stdout.read().decode("utf-8")
        ssh.close()
        
        return result
    except Exception as e:
        print(f"[ERROR] {e}")
        return None


# ===== EXEMPLE DE UTILIZARE =====

# 1. Notificare simpla
if __name__ == "__main__":
    # Send test notification
    result = send_ntfy_notification("Test notification from Python!")
    
    # Send backup notification
    send_ntfy_notification("Backup completed successfully!")
    
    # Send alert
    send_ntfy_notification("ALERT: High CPU usage detected!")
    
    print("[INFO] Notificari trimise!")
    
    # Pentru cron jobs
    print("\n[Cron Example]")
    print("0 0 * * * /usr/local/bin/ntfy_notify.sh 'Backup zilnic completat!'")
    
    # Pentru backup scripts
    print("\n[Backup Example]")
    print("# In backup script:")
    print("/usr/local/bin/ntfy_notify.sh \"Backup completed: ${timestamp}\"")

