import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)

from config import BOT_TOKEN
from database import init_db
from handlers import (
    start_command,
    show_categories,
    show_products,
    back_to_categories,
    my_cart_callback,
    support_callback,
    start_payment,
    confirm_payment_method,
    validate_order,
    refuse_order,
    add_product_start,
    add_product_category,
    add_product_name,
    add_product_description,
    add_product_price,
    add_product_cancel,
    remove_product_command,
    CATEGORY,
    NAME,
    DESCRIPTION,
    PRICE,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

async def post_init(application: Application):
    await init_db()

def main():
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    # Commandes de base
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("supprimer", remove_product_command))

    # Navigation catalogue
    app.add_handler(CallbackQueryHandler(show_categories, pattern="^categories$"))
    app.add_handler(CallbackQueryHandler(show_products, pattern="^cat_"))
    app.add_handler(CallbackQueryHandler(back_to_categories, pattern="^back_categories$"))
    app.add_handler(CallbackQueryHandler(my_cart_callback, pattern="^cart$"))
    app.add_handler(CallbackQueryHandler(support_callback, pattern="^support$"))

    # Paiement
    app.add_handler(CallbackQueryHandler(start_payment, pattern="^buy_"))
    app.add_handler(CallbackQueryHandler(confirm_payment_method, pattern="^pay_"))
    app.add_handler(CallbackQueryHandler(validate_order, pattern="^valid_"))
    app.add_handler(CallbackQueryHandler(refuse_order, pattern="^refuse_"))

    # Ajout de produit (admin uniquement)
    add_product_conversation = ConversationHandler(
        entry_points=[CommandHandler("ajouter", add_product_start)],
        states={
            CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_product_category)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_product_name)],
            DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_product_description)],
            PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_product_price)],
        },
        fallbacks=[CommandHandler("annuler", add_product_cancel)],
    )
    app.add_handler(add_product_conversation)

    print("Bot démarré...")
    app.run_polling()

if __name__ == "__main__":
    main()
