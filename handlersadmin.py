from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from config import ADMIN_ID

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Vous n'êtes pas autorisé.")
        return

    keyboard = [
        ["➕ Ajouter un produit", "✏️ Modifier un produit"],
        ["🗑 Supprimer un produit", "📦 Voir les produits"],
        ["🛒 Voir les commandes", "📊 Statistiques"],
        ["💳 Paiements", "🏠 Retour"]
    ]

    await update.message.reply_text(
        "👨‍💼 Panneau d'administration DIGITAL Market Gaming",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
    )async def addproduct(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Accès refusé.")
        return

    await update.message.reply_text(
        "📦 Fonction en cours de développement.\n\n"
        "Bientôt, tu pourras ajouter un produit directement depuis Telegram."
    )