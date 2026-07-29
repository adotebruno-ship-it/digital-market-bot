from database import init_db
app.run_polling()
init_db()
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
    ["🎮 Jeux PS2", "🎮 Jeux PS3"],
    ["🎮 Jeux PS4", "🎮 Jeux PS5"],
    ["🎮 PSP", "🎮 PS Vita"],
    ["🎮 Nintendo", "💻 Jeux PC"],
    ["📱 Jeux Android", "🕹 Consoles"],
    ["🎮 Manettes", "🎧 Accessoires"],
    ["💳 Abonnements", "🔍 Rechercher"],
    ["🛒 Panier", "📦 Mes commandes"],
    ["📞 Support"]
]
    

    await update.message.reply_text(
    "🎮 Bienvenue sur DIGITAL Market Gaming\n\n"
    "Votre boutique de jeux vidéo et d'accessoires.\n\n"
    "Sélectionnez une catégorie :",
    reply_markup=ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )
)
        
        )
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("DIGITAL Market Gaming est lancé...")
    app.run_polling()

if __name__ == "__main__":
    main()
    from handlers.admin import admin
from telegram.ext import CommandHandler
app.add_handler(CommandHandler("admin", admin))
from handlers.admin import admin, addproduct
app.add_handler(CommandHandler("addproduct", addproduct))