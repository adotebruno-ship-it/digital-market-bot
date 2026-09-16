"""
Configuration centrale du bot.
Toutes les valeurs sensibles viennent des variables d'environnement
(fichier .env en local, "Variables" sur Railway) — jamais écrites en dur ici.
"""

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")  # ton ID Telegram, pour recevoir les commandes
WAVE_NUMBER = os.getenv("WAVE_NUMBER", "Non configuré")
ORANGE_MONEY_NUMBER = os.getenv("ORANGE_MONEY_NUMBER", "Non configuré")

DB_PATH = "data/shop.db"

# Catégories du magasin. Adapte librement à ce que tu vends réellement
# (produits physiques, accessoires, codes d'abonnement achetés légitimement, etc.)
CATEGORIES = [
    "🕹 Consoles",
    "🎮 Manettes",
    "🎧 Accessoires",
    "💳 Abonnements",
]

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN manquant. Ajoute-le dans ton fichier .env (local) "
        "ou dans les Variables Railway (production)."
    )
