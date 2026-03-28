#!/bin/bash
# ─────────────────────────────────────────
# setup.sh — Initialise le repo IAM-Demo
# Usage : bash setup.sh
# ─────────────────────────────────────────

echo "Initialisation du repo IAM-Demo..."

# Init git
git init
git branch -M main

# Créer config.py local (non committé)
if [ ! -f "Python/config.py" ]; then
cat > Python/config.py << 'EOF'
# Credentials Auth0 — ne jamais commiter ce fichier
AUTH0_CLIENT_ID     = "TON_CLIENT_ID"
AUTH0_CLIENT_SECRET = "TON_CLIENT_SECRET"
EOF
echo "config.py créé dans Python/ — remplis tes credentials"
fi

# Premier commit
git add .
git commit -m "init: projet IAM-Demo JML SailPoint + Python Auth0"

echo ""
echo "Repo initialisé. Pour pousser sur GitHub :"
echo "  git remote add origin https://github.com/TON_USERNAME/IAM-Demo.git"
echo "  git push -u origin main"
