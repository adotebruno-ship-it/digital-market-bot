from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

import database as db
from config import WAVE_NUMBER, ORANGE_MONEY_NUMBER, ADMIN_CHAT_ID


async def start_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    product_id = int(query.data.split(":", 1)[1])

    product = await db.get_product(product_id)
    if not product:
        await query.edit_message_text("Ce produit n'est plus disponible.")
        return

    _, category, name, description, price = product

    order_id = await db.create_order(
        user_id=query.from_user.id,
        username=query.from_user.username or query.from_user.first_name,
        product_id=product_id,
    )

    text = (
        f"🧾 Commande #{order_id} — {name}\n"
        f"💰 Montant : {price} FCFA\n\n"
        f"💳 Effectue le paiement à l'un de ces numéros :\n"
        f"📱 Wave : {WAVE_NUMBER}\n"
        f"📱 Orange Money : {ORANGE_MONEY_NUMBER}\n\n"
        f"Une fois payé, appuie sur le bouton ci-dessous puis envoie la "
        f"capture d'écran de la transaction directement dans ce chat."
    )
    keyboard = [
        [InlineKeyboardButton("✅ J'ai payé", callback_data=f"paid:{order_id}")],
        [InlineKeyboardButton("⬅️ Annuler", callback_data="back_to_menu")],
    ]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def confirm_paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Le client indique avoir payé : on prévient l'administrateur pour validation manuelle."""
    query = update.callback_query
    await query.answer()
    order_id = int(query.data.split(":", 1)[1])

    order = await db.get_order(order_id)
    if not order:
        await query.edit_message_text("Commande introuvable.")
        return

    _, user_id, username, product_id, status = order
    product = await db.get_product(product_id)
    _, category, name, description, price = product

    await query.edit_message_text(
        "✅ Merci ! Ta preuve de paiement a été transmise.\n"
        "Nous validons manuellement chaque commande — tu recevras un message "
        "dès que ton produit sera confirmé."
    )

    if ADMIN_CHAT_ID:
        admin_text = (
            f"🔔 Nouvelle commande à valider\n\n"
            f"Commande : #{order_id}\n"
            f"Client : @{username} (id {user_id})\n"
            f"Produit : {name}\n"
            f"Prix : {price} FCFA\n\n"
            f"Vérifie la preuve de paiement envoyée par le client, puis valide ci-dessous."
        )
        keyboard = [
            [
                InlineKeyboardButton("✅ Valider", callback_data=f"validate:{order_id}"),
                InlineKeyboardButton("❌ Refuser", callback_data=f"refuse:{order_id}"),
            ]
        ]
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


async def validate_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Réservé à l'administrateur : confirme la commande après vérification du paiement."""
    query = update.callback_query
    await query.answer()

    if str(query.from_user.id) != str(ADMIN_CHAT_ID):
        await query.answer("Action réservée à l'administrateur.", show_alert=True)
        return

    order_id = int(query.data.split(":", 1)[1])
    order = await db.get_order(order_id)
    if not order:
        await query.edit_message_text("Commande introuvable.")
        return

    _, user_id, username, product_id, status = order
    await db.set_order_status(order_id, "validee")

    await query.edit_message_text(f"✅ Commande #{order_id} validée.")

    await context.bot.send_message(
        chat_id=user_id,
        text=(
            f"🎉 Ta commande #{order_id} est validée !\n\n"
            f"Le vendeur va te contacter ici même pour organiser la livraison "
            f"(remise en main propre, envoi, ou code d'activation selon le produit)."
        ),
    )


async def refuse_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Réservé à l'administrateur : refuse une commande (paiement non reçu/invalide)."""
    query = update.callback_query
    await query.answer()

    if str(query.from_user.id) != str(ADMIN_CHAT_ID):
        await query.answer("Action réservée à l'administrateur.", show_alert=True)
        return

    order_id = int(query.data.split(":", 1)[1])
    order = await db.get_order(order_id)
    if not order:
        await query.edit_message_text("Commande introuvable.")
        return

    _, user_id, username, product_id, status = order
    await db.set_order_status(order_id, "refusee")

    await query.edit_message_text(f"❌ Commande #{order_id} refusée.")

    await context.bot.send_message(
        chat_id=user_id,
        text=(
            f"❌ Ta commande #{order_id} n'a pas pu être validée.\n"
            f"Contacte le support si tu penses qu'il s'agit d'une erreur."
        ),
    )
