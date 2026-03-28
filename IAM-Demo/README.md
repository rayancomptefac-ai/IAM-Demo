# IAM-Demo

Projet de démonstration d'un cycle JML (Joiner/Mover/Leaver) complet 
implémenté avec SailPoint IIQ (BeanShell/XML) et Python (Auth0 API REST).

Réalisé dans le cadre d'une préparation à une alternance consultant IAM.

## Stack technique
- SailPoint IIQ — Rules BeanShell, Workflow XML
- Python 3 — provisioning automatisé via API REST
- Auth0 — Identity Provider, flux OAuth2 Client Credentials
- Active Directory — application cible simulée

## Structure du projet

### SailPoint/
| Fichier | Type | Description |
|---|---|---|
| Rule-Library-BankSecure.xml | Library | Méthodes réutilisables — genererLogin(), genererEmail() |
| Rule-Joiner-GenerateLogin.xml | AttributeGenerator | Génère le login depuis prénom + nom |
| Rule-Joiner-GenerateEmail.xml | AttributeGenerator | Génère l'email selon le type de contrat |
| Rule-Leaver-DisableAccount.xml | Leaver | Désactive l'Identity lors d'un départ |
| Rule-Correlation-BankSecure.xml | Correlation | Corrèle les comptes AD aux Identities SailPoint |
| Workflow-Joiner-BankSecure.xml | Subprocess | Orchestre le cycle Joiner complet |

### Python/
| Fichier | Description |
|---|---|
| onboarding.py | Script JML complet — Joiner, Mover, Leaver via Auth0 API |

## Logique métier
- Login : initiale prénom + nom nettoyé, max 20 caractères
- Email : login + domaine selon contrat
  - Stagiaire → @extern.banksecure.fr
  - CDI / CDD → @banksecure.fr
- Désactivation : `blocked: True` via Auth0 PATCH, `inactive: true` via SailPoint

## Lancer le script Python

**1. Créer un fichier `config.py` avec tes credentials Auth0 :**
```python
AUTH0_CLIENT_ID     = "ton_client_id"
AUTH0_CLIENT_SECRET = "ton_client_secret"
```

**2. Installer les dépendances :**
```bash
pip install requests
```

**3. Lancer :**
```bash
python onboarding.py
```

## Ordre d'import SailPoint
```
1. Rule-Library-BankSecure.xml
2. Rule-Joiner-GenerateLogin.xml
3. Rule-Joiner-GenerateEmail.xml
4. Rule-Leaver-DisableAccount.xml
5. Rule-Correlation-BankSecure.xml
6. Workflow-Joiner-BankSecure.xml
```

## Auteur
Rayan Sadouki
