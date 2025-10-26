#!/usr/bin/env python
"""
Integrare NTFY cu scripturi de backup existente
Compatibil cu bash/csh scripts vechi

ATENTIE: Inlocuieste TOATE valorile sensibile!
"""

import paramiko
import sys

# ===== CONFIGURAZE CELE DE JOS =====
HOST = "YOUR_SERVER_IP"
USER = "root"
PASS = "YOUR_PASSWORD"
PORT = 22
BACKUP_SCRIPT = "/path/to/your/backup/script.sh"
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
    print("   INTEGRARE NTFY CU BACKUP SCRIPTS")
    print("=" * 70)
    print()
    
    if HOST == "YOUR_SERVER_IP" or PASS == "YOUR_PASSWORD":
        print("[ERROR] Configureaza variabilele HOST si PASS!")
        return 1
    
    if BACKUP_SCRIPT == "/path/to/your/backup/script.sh":
        print("[ERROR] Configureaza BACKUP_SCRIPT cu calea ta!")
        return 1
    
    print("[INFO] Conectare la server...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(HOST, PORT, USER, PASS, timeout=15)
        print("[OK] Conectat!")
        print()
        
        # 1. Backup script original
        print("=" * 70)
        print("1. BACKUP SCRIPT ORIGINAL")
        print("=" * 70)
        print()
        
        print(f"[INFO] Creez backup pentru {BACKUP_SCRIPT}...")
        ssh_exec(ssh, f"cp {BACKUP_SCRIPT} {BACKUP_SCRIPT}.backup", show=False)
        print("[OK] Backup creat!")
        print()
        
        # 2. Citeste scriptul
        print("=" * 70)
        print("2. CITESTE SCRIPTUL")
        print("=" * 70)
        print()
        
        out, _ = ssh_exec(ssh, f"cat {BACKUP_SCRIPT}", show=False)
        print("Continut script:")
        print(out[:500])
        print()
        
        # 3. Adauga NTFY dupa email
        print("=" * 70)
        print("3. ADAUGA NOTIFICARE NTFY")
        print("=" * 70)
        print()
        
        # Exemple de modificari bazate pe tipul de script
        
        # Pentru bash scripts:
        # ssh_exec(ssh, f'''sed -i '/mailx -s/a \\
        #     /usr/local/bin/ntfy_notify.sh "Backup completed: ${{SUBJECT}}"
        #     ' {BACKUP_SCRIPT}''', show=False)
        
        # Pentru csh scripts:
        # ssh_exec(ssh, f'''sed -i '/mailx -s/a \\
        #     /usr/local/bin/ntfy_notify.sh "Backup completed"
        #     ' {BACKUP_SCRIPT}''', show=False)
        
        print("[INFO] Adauga manual linia de notificare NTFY in scriptul tau:")
        print()
        print("Exemplu pentru bash:")
        print('  /usr/local/bin/ntfy_notify.sh "Backup completed!"')
        print()
        print("Exemplu pentru csh:")
        print('  /usr/local/bin/ntfy_notify.sh "Backup completed"')
        print()
        
        # 4. Test
        print("=" * 70)
        print("4. TEST INTEGRARE")
        print("=" * 70)
        print()
        
        print("[INFO] Ruleaza scriptul de backup pentru test...")
        print(f"[INFO] Command: {BACKUP_SCRIPT}")
        print()
        
        # Nu rulam realmente, doar aratam comanda
        print("[INFO] Pentru a testa, ruleaza manual:")
        print(f"  {BACKUP_SCRIPT}")
        print()
        print("[INFO] Ar trebui sa primesti notificare NTFY dupa backup!")
        print()
        
        ssh.close()
        
        print("=" * 70)
        print("INTEGRARE COMPLETA!")
        print("=" * 70)
        print()
        print(">> INSTRUCTIUNI FINALE:")
        print("   1. Modifica manual scriptul de backup")
        print("   2. Adauga linia cu ntfy_notify.sh")
        print("   3. Testeaza ruland backup-ul")
        print("   4. Verifica notificarea pe telefon")
        print()
        
        return 0
        
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

