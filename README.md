# DIGITAL Market Gaming — Bot Telegram

Bot boutique Telegram : consoles, manettes, accessoires et abonnements.
Paiement via Wave / Orange Money (validation manuelle par l'administrateur).

## ⚠️ Important

Ce bot livre uniquement des produits légitimes : produits physiques
(consoles, manettes, accessoires) ou codes d'abonnement officiels que
tu as toi-même achetés légalement. Il n'automatise pas l'envoi de
fichiers de jeux protégés par le droit d'auteur — la livraison se fait
manuellement, en discutant avec le client après validation du paiement.

## Installation locale

1. Installe les dépendances :
   ```
   pip install -r requirements.txt
   ```
2. Copie `.env.example` en `.env` et remplis tes vraies valeurs :
   ```
   BOT_TOKEN=...
   ADMIN_CHAT_ID=...
   WAVE_NUMBER=...
   ORANGE_MONEY_NUMBER=...
   ```
3. Lance le bot :
   ```
   python main.py
   ```

## Trouver ton ADMIN_CHAT_ID

Envoie un message à [@userinfobot](https://t.me/userinfobot) sur Telegram :
il te répond avec ton ID numérique. C'est cette valeur qu'il faut mettre
dans `ADMIN_CHAT_ID` pour recevoir les notifications de commande et
pouvoir valider/refuser les paiements.

## Déploiement sur Railway

1. Pousse ce projet sur GitHub (`git add . && git commit -m "init" && git push`).
2. Sur [railway.app](https://railway.app), clique sur **New Project** →
   **Deploy from GitHub Repo** → sélectionne ton dépôt.
3. Dans l'onglet **Variables** du projet Railway, ajoute :
   - `BOT_TOKEN`
   - `ADMIN_CHAT_ID`
   - `WAVE_NUMBER`
   - `ORANGE_MONEY_NUMBER`
4. Railway installe les dépendances et lance `python main.py`
   automatiquement (voir `Procfile`).

## Commandes admin

- `/ajouter` — ajoute un produit au catalogue (conversation guidée :
  catégorie, nom, description, prix).
- `/supprimer <id>` — retire un produit du catalogue.

## Catégories par défaut

Modifiables dans `config.py` (`CATEGORIES`) :
- 🕹 Consoles
- 🎮 Manettes
- 🎧 Accessoires
- 💳 Abonnements

## Structure du projet

```
digital-market-bot/
├── main.py              # point d'entrée, assemble tous les handlers
├── config.py             # variables d'environnement, catégories
├── database.py           # SQLite : produits et commandes
├── requirements.txt
├── Procfile               # commande de démarrage pour Railway
├── .env.example
└── handlers/
    ├── start.py           # menu principal
    ├── products.py        # navigation catalogue
    ├── payments.py        # paiement Wave/Orange Money + validation admin
    └── admin.py           # ajout/suppression de produits
```
