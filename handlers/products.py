from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

import database as db


async def show_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data.split(":", 1)[1]

    products = await db.get_products_by_category(category)

    if not products:
        await query.edit_message_text(
            f"{category}\n\nAucun produit disponible pour le moment.",
            reply_markup=_back_keyboard(),
        )
        return

    keyboard = [
        [InlineKeyboardButton(f"{name} — {price} FCFA", callback_data=f"product:{pid}")]
        for pid, name, price in products
    ]
    keyboard.append([InlineKeyboardButton("⬅️ Retour", callback_data="back_to_menu")])

    await query.edit_message_text(
        f"{category}\n\nChoisis un produit :",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def show_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    product_id = int(query.data.split(":", 1)[1])

    product = await db.get_product(product_id)
    if not product:
        await query.edit_message_text("Ce produit n'est plus disponible.")
        return

    _, category, name, description, price = product

    text = (
        f"🛒 {name}\n\n"
        f"{description or ''}\n\n"
        f"💰 Prix : {price} FCFA"
    )
    keyboard = [
        [InlineKeyboardButton("✅ Commander", callback_data=f"buy:{product_id}")],
        [InlineKeyboardButton("⬅️ Retour", callback_data=f"cat:{category}")],
    ]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from handlers.start import start
    await start(update, context)


async def my_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    orders = await db.get_user_orders(query.from_user.id)

    if not orders:
        text = "📦 Tu n'as pas encore de commande."
    else:
        lines = ["📦 Tes commandes :\n"]
        for order_id, product_name, status, created_at in orders:
            lines.append(f"#{order_id} — {product_name} — {status}")
        text = "\n".join(lines)

    await query.edit_message_text(text, reply_markup=_back_keyboard())


def _back_keyboard():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("⬅️ Retour au menu", callback_data="back_to_menu")]]
    )
