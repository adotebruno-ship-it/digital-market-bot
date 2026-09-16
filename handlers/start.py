from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from config import CATEGORIES


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(cat, callback_data=f"cat:{cat}")]
        for cat in CATEGORIES
    ]
    keyboard.append([InlineKeyboardButton("📦 Mes commandes", callback_data="my_orders")])
    keyboard.append([InlineKeyboardButton("📞 Support", callback_data="support")])

    text = (
        "🛒 Bienvenue sur DIGITAL Market Gaming !\n\n"
        "Consoles, manettes, accessoires et abonnements officiels.\n"
        "Choisis une catégorie ci-dessous :"
    )

    if update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "📞 Besoin d'aide ?\n\n"
        "Écris-nous directement ici et un membre de l'équipe te répondra."
    )
