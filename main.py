import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)

from config import BOT_TOKEN
from database import init_db
import handlers

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

async def post_init(application: Application):
    await init_db()

def main():
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    # Commandes de base
    app.add_handler(CommandHandler("start", handlers.start_command))
    if hasattr(handlers, "remove_product_command"):
        app.add_handler(CommandHandler("supprimer", handlers.remove_product_command))

    # Navigation catalogue
    app.add_handler(CallbackQueryHandler(handlers.show_categories, pattern="^categories$"))
    app.add_handler(CallbackQueryHandler(handlers.show_products, pattern="^cat_"))
    app.add_handler(CallbackQueryHandler(handlers.back_to_categories, pattern="^back_categories$"))
    app.add_handler(CallbackQueryHandler(handlers.my_cart_callback, pattern="^cart$"))
    app.add_handler(CallbackQueryHandler(handlers.support_callback, pattern="^support$"))

    # Paiement
    app.add_handler(CallbackQueryHandler(handlers.start_payment, pattern="^buy_"))
    app.add_handler(CallbackQueryHandler(handlers.confirm_payment_method, pattern="^pay_"))
    app.add_handler(CallbackQueryHandler(handlers.validate_order, pattern="^valid_"))
    app.add_handler(CallbackQueryHandler(handlers.refuse_order, pattern="^refuse_"))

    # Ajout de produit (admin uniquement)
    if hasattr(handlers, "add_product_start"):
        add_product_conversation = ConversationHandler(
            entry_points=[CommandHandler("ajouter", handlers.add_product_start)],
            states={
                handlers.CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.add_product_category)],
                handlers.NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.add_product_name)],
                handlers.DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.add_product_description)],
                handlers.PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.add_product_price)],
            },
            fallbacks=[CommandHandler("annuler", handlers.add_product_cancel)],
        )
        app.add_handler(add_product_conversation)

    print("Bot démarré...")
    app.run_polling()

if __name__ == "__main__":
    main()
