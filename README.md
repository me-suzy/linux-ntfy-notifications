# Linux Server Notifications Setup

Colectie de scripturi pentru configurare notificari pe servere Linux vechi (compatibile cu OpenSSL 0.9.7a, curl 7.12.1, Python 2.7).

## Caracteristici

- ✅ Compatibil cu servere Linux vechi (RHEL 4, Debian old-stable)
- ✅ NTFY pentru notificari GRATIS
- ✅ Nu necesita instalari pe server (foloseste curl existent)
- ✅ Notificari instant pe telefon
- ✅ Compatibil cu curl 7.12.1 si OpenSSL 0.9.7a
- ✅ Setup in 5 minute

## Instalare

### 1. Configurare Local

Inlocuieste valorile in scripturi:
```python
HOST = "YOUR_SERVER_IP"
PASS = "YOUR_PASSWORD"
```

### 2. Ruleaza Setup

```bash
python setup_ntfy_notifications.py
```

### 3. Instaleaza Aplicatia NTFY pe Telefon

- **Android**: https://play.google.com/store/apps/details?id=io.heckel.ntfy
- **iOS**: https://apps.apple.com/app/ntfy/id1625396347

### 4. Subscribe la Topic

In aplicatia NTFY, adauga topic-ul afisat de script.

## Utilizare

### Notificari Manuale

```bash
/usr/local/bin/ntfy_notify.sh "Mesajul tau"
```

### Pentru Cron Jobs

```bash
0 0 * * * /usr/local/bin/ntfy_notify.sh "Backup completat!"
```

### Pentru Backup Scripts

Adauga in scriptul de backup:

```bash
echo "Backup completat!" | /usr/local/bin/ntfy_notify.sh
```

## Compatibilitate

Testat pe:
- Red Hat Enterprise Linux ES release 4 (Nahant Update 8)
- Kernel: 2.6.9-89.ELsmp
- OpenSSL: 0.9.7a
- curl: 7.12.1
- Python: 2.7.x

## Fisiere Incluse

- `setup_ntfy_notifications.py` - Script principal de setup NTFY
- `integrate_with_backup.py` - Integrare cu backup scripts existente
- `README.md` - Documentatie (acest fisier)

## Notificari

Notificarile sunt trimise prin **NTFY**, un serviciu FREE pentru notificari push:
- GRATUIT
- Fara limitari
- Instant delivery
- Compatibil cu toate platformele

## Securitate

⚠️ **IMPORTANT**: Inlocuieste TOATE valorile sensibile inainte de utilizare:
- IP-uri de servere
- Parole
- Tokeni
- Credentiale

Aceste scripturi sunt template-uri pentru dezvoltare. Nu folosi credentialele din exemple!

## Licenta

Acest cod este oferit "AS IS", fara garantii. Poti folosi, modifica si distribui liber.

## Contribuții

Contribuțiile sunt binevenite! Te rugam sa:
- Inlocuiesti TOATE datele sensibile
- Testezi scripturile pe servere vechi
- Documentezi modificari

## Support

Pentru probleme sau intrebari:
- Verifica logs: `tail -f /var/log/messages`
- Testeaza notificari: `/usr/local/bin/ntfy_notify.sh "Test"`
- Verifica cron: `crontab -l`

## Alternativa

Daca NTFY nu functioneaza din cauza limitarilor firewall-ului:
- Foloseste email (sendmail)
- Configureaza Slack webhooks
- Foloseste Discord webhooks

## Exemple de Utilizare

### Backup Daily

```bash
0 0 * * * /usr/local/bin/ntfy_notify.sh "Backup zilnic completat!"
```

### Monitoring

```bash
*/5 * * * * /usr/local/bin/ntfy_notify.sh "Server OK - $(date)"
```

### Alerts

```bash
echo "Eroare critica!" | /usr/local/bin/ntfy_notify.sh
```

## Note

- NTFY foloseste HTTP (nu HTTPS) pentru compatibilitate cu serverele vechi
- Notificarile pot avea o intarziere de cateva secunde
- Nu necesita instalari pe server (doar curl)
- GRATUIT pentru utilizare nelimitata

---

Made with ❤️ for old Linux servers

