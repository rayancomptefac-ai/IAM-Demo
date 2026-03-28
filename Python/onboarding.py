import requests
from config import AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET

AUTH0_DOMAIN = "https://dev-4mv3patcf33iaw0l.eu.auth0.com"

# ─────────────────────────────────────────
# UTILS
# ─────────────────────────────────────────

def genererLogin(prenom, nom):
    if prenom is None or prenom == "":
        return "inconnu"
    if nom is None or nom == "":
        return "inconnu"
    prenomClean = prenom.lower().replace("-", "").replace(" ", "")
    nomClean    = nom.lower().replace("-", "").replace(" ", "")
    initiale    = prenomClean[0]
    loginBrut   = initiale + nomClean
    if len(loginBrut) > 20:
        return loginBrut[:20]
    return loginBrut

# ─────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────

def get_token():
    url = f"{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "client_id":     AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "audience":      f"{AUTH0_DOMAIN}/api/v2/",
        "grant_type":    "client_credentials"
    }
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        return data["access_token"]
    except requests.exceptions.ConnectionError:
        print("Erreur — Auth0 indisponible")
        return None
    except Exception as e:
        print(f"Erreur inattendue — {e}")
        return None

# ─────────────────────────────────────────
# JOINER
# ─────────────────────────────────────────

def create_user(token, employe):
    url = f"{AUTH0_DOMAIN}/api/v2/users"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type":  "application/json"
    }
    login = genererLogin(employe["prenom"], employe["nom"])
    email = login + "@banksecure.fr"
    name  = employe["prenom"] + " " + employe["nom"]
    payload = {
        "email":      email,
        "name":       name,
        "nickname":   login,
        "connection": "Username-Password-Authentication",
        "password":   "Synetis2026!",
        "app_metadata": {
            "department":   employe["department"],
            "contractType": employe["contractType"],
        }
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        print(f"✓ JOINER  {login} — {data.get('user_id', data.get('message', 'erreur'))}")
    except Exception as e:
        print(f"✗ JOINER  {login} — Erreur : {e}")

# ─────────────────────────────────────────
# MOVER
# ─────────────────────────────────────────

def modify_user(token, user_id, modifications):
    url = f"{AUTH0_DOMAIN}/api/v2/users/{user_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type":  "application/json"
    }
    try:
        response = requests.patch(url, headers=headers, json=modifications)
        data = response.json()
        print(f"✓ MOVER   {user_id} — {data.get('app_metadata', 'erreur')}")
    except Exception as e:
        print(f"✗ MOVER   {user_id} — Erreur : {e}")

# ─────────────────────────────────────────
# LEAVER
# ─────────────────────────────────────────

def disable_user(token, user_id):
    url = f"{AUTH0_DOMAIN}/api/v2/users/{user_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type":  "application/json"
    }
    try:
        response = requests.patch(url, headers=headers, json={"blocked": True})
        data = response.json()
        if data.get("blocked"):
            print(f"✓ LEAVER  {user_id} — désactivé")
        else:
            print(f"✗ LEAVER  {user_id} — erreur : {data.get('message', 'inconnue')}")
    except Exception as e:
        print(f"✗ LEAVER  {user_id} — Erreur : {e}")

# ─────────────────────────────────────────
# FLUX RH
# ─────────────────────────────────────────

flux_rh = [
    {"prenom": "Élodie",  "nom": "Martin",    "department": "RH",           "contractType": "CDI"},
    {"prenom": "Ali",     "nom": "Ben Salah", "department": "Informatique", "contractType": "CDD"},
]

def run_onboarding():
    token = get_token()
    if token is None:
        print("Token non récupéré — arrêt du Joiner")
        return
    for employe in flux_rh:
        create_user(token, employe)

def run_modify():
    token = get_token()
    if token is None:
        print("Token non récupéré — arrêt du Mover")
        return
    modify_user(token, "auth0|TON_USER_ID", {"app_metadata": {"department": "Finance"}})

def run_disable():
    token = get_token()
    if token is None:
        print("Token non récupéré — arrêt du Leaver")
        return
    disable_user(token, "auth0|TON_USER_ID")

# ─────────────────────────────────────────
# POINT D'ENTRÉE
# ─────────────────────────────────────────

run_onboarding()
# run_modify()
# run_disable()
