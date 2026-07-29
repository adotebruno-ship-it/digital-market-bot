from telegram import Update
from telegram.ext import ContextTypes

products = {
    "ps2": [
        {"name": "God of War 2", "price": 3000},
        {"name": "GTA San Andreas", "price": 2500},
    ],
    "ps3": [
        {"name": "GTA V", "price": 5000},
        {"name": "The Last of Us", "price": 5000},
    ],
    "ps4": [
        {"name": "FC 26", "price": 10000},
        {"name": "Red Dead Redemption 2", "price": 8000},
    ]
}

async def show_ps2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🎮 Jeux PS2\n\n"
    for game in products["ps2"]:
        text += f"• {game['name']} - {game['price']} FCFA\n"
    await update.message.reply_text(text)