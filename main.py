import asyncio

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN
from database import init_db

from handlers.start import start, support
from handlers.products import show_category, show_product, back_to_menu, my_orders
from handlers.payments import start_payment, confirm_paid, validate_order, refuse_order
from handlers.admin import (
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


def main():
    

    app = Application.builder().token(BOT_TOKEN).build()

    # Commandes de base
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("supprimer", remove_product_command))

    # Navigation catalogue
    app.add_handler(CallbackQueryHandler(show_category, pattern=r"^cat:"))
    app.add_handler(CallbackQueryHandler(show_product, pattern=r"^product:"))
    app.add_handler(CallbackQueryHandler(back_to_menu, pattern=r"^back_to_menu$"))
    app.add_handler(CallbackQueryHandler(my_orders, pattern=r"^my_orders$"))
    app.add_handler(CallbackQueryHandler(support, pattern=r"^support$"))

    # Paiement
    app.add_handler(CallbackQueryHandler(start_payment, pattern=r"^buy:"))
    app.add_handler(CallbackQueryHandler(confirm_paid, pattern=r"^paid:"))
    app.add_handler(CallbackQueryHandler(validate_order, pattern=r"^validate:"))
    app.add_handler(CallbackQueryHandler(refuse_order, pattern=r"^refuse:"))

    # Ajout de produit (admin uniquement) : conversation guidée
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
    asyncio.run(init_db())
    main()

