# Deployment-Dokumentation: Evennia + GitHub + Debian (Nginx/SSL)

## Überblick
- **Repo:** `git@github.com:peddn/timepit.git` (privat)
- **Spiel-User:** `mud` (Evennia läuft unter diesem Account)
- **Spielverzeichnis:** `/var/lib/mud/timepit`
- **Deploy-Skript:** `/var/lib/mud/deploy.sh`
- **Wrapper:** `/usr/local/bin/deploy_timepit` (führt Deploy als `mud` aus)
- **Server-SSH:** Deploy-Key **read-only** für GitHub (nur Pull)
- **Deployment:** manuell per `deploy_timepit`

---

## Rollen & Schlüssel

### Entwickler
- Jeder hat einen eigenen SSH-Key im GitHub-Account.
- Rechte: **push & pull**.
- Workflow: lokal entwickeln → nach GitHub pushen.

### Server
- Benutzer: `mud`
- SSH-Key: **Deploy-Key (Read-Only)** im Repo (*Settings → Deploy keys*)
- Zweck: **nur pull** vom Repo

---

## Branch-/Git-Policy
- Es gibt nur den Branch **`main`**.
- `main` ist immer **deploybar**.
- Vor jeder Änderung lokal:
```bash
git pull --ff-only
```

---

## Entwickler-Workflow (lokal)

```bash
git switch main
git pull --ff-only

# Änderungen machen
git add -A
git commit -m "Beschreibung"
git push
```

> Einmalig empfohlen:
> `git config --global pull.ff only`
> `git config --global push.autoSetupRemote true`

---

## Server-Workflow (Deployment)

**Ziel:** Server spiegelt exakt `origin/main`.

```bash
deploy_timepit
```

### `/var/lib/mud/deploy.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

cd /var/lib/mud/timepit

# venv aktivieren (falls vorhanden)
if [ -f /var/lib/mud/.venv/bin/activate ]; then
    source /var/lib/mud/.venv/bin/activate
fi

git pull --ff-only

if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

evennia reload || evennia restart

echo "Deploy erfolgreich abgeschlossen."
```

**Rechte (als root einmalig):**

```bash
chown mud:mud /var/lib/mud/deploy.sh
chmod 750 /var/lib/mud/deploy.sh
```

---

## Wrapper für einfachen Aufruf

`/usr/local/bin/deploy_timepit` (als root anlegen):

```bash
#!/bin/sh
exec sudo -u mud /var/lib/mud/deploy.sh
```

Rechte setzen:

```bash
chmod 755 /usr/local/bin/deploy_timepit
```

---

## SSH-Config auf dem Server (falls Key nicht Standardname)

Unter `mud`, Datei `~/.ssh/config`:

```
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_deploy
    IdentitiesOnly yes
```
