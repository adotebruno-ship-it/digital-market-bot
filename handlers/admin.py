from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

import database as db
from config import ADMIN_CHAT_ID, CATEGORIES

# États de la conversation d'ajout de produit
CATEGORY, NAME, DESCRIPTION, PRICE = range(4)


def _is_admin(update: Update) -> bool:
    return str(update.effective_user.id) == str(ADMIN_CHAT_ID)


async def add_product_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update):
        await update.message.reply_text("Cette commande est réservée à l'administrateur.")
        return ConversationHandler.END

    cats = "\n".join(CATEGORIES)
    await update.message.reply_text(
        f"Ajout d'un produit.\n\nCatégories disponibles :\n{cats}\n\n"
        f"Envoie le nom exact de la catégorie (copie-colle une ligne ci-dessus)."
    )
    return CATEGORY


async def add_product_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["new_product_category"] = update.message.text.strip()
    await update.message.reply_text("Nom du produit ?")
    return NAME


async def add_product_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["new_product_name"] = update.message.text.strip()
    await update.message.reply_text("Description courte du produit ?")
    return DESCRIPTION


async def add_product_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["new_product_description"] = update.message.text.strip()
    await update.message.reply_text("Prix en FCFA (nombre uniquement) ?")
    return PRICE


async def add_product_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        price = int(update.message.text.strip())
    except ValueError:
        await update.message.reply_text("Merci d'envoyer un nombre valide, ex: 15000")
        return PRICE

    await db.add_product(
        category=context.user_data["new_product_category"],
        name=context.user_data["new_product_name"],
        description=context.user_data["new_product_description"],
        price=price,
    )

    await update.message.reply_text(
        f"✅ Produit ajouté : {context.user_data['new_product_name']} — {price} FCFA"
    )
    context.user_data.clear()
    return ConversationHandler.END


async def add_product_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("Ajout de produit annulé.")
    return ConversationHandler.END


async def remove_product_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Usage : /supprimer <id_produit>"""
    if not _is_admin(update):
        await update.message.reply_text("Cette commande est réservée à l'administrateur.")
        return

    if not context.args:
        await update.message.reply_text("Usage : /supprimer <id_produit>")
        return

    try:
        product_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("L'id du produit doit être un nombre.")
        return

    await db.remove_product(product_id)
    await update.message.reply_text(f"🗑 Produit #{product_id} retiré du catalogue.")
