import os,sqlite3
from telegram import Update,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Application,CommandHandler,ContextTypes,MessageHandler,CallbackQueryHandler,ConversationHandler,filters

TOKEN=os.getenv("BOT_TOKEN"); ADMIN_ID=int(os.getenv("ADMIN_ID","7256987382"))
WAVE=os.getenv("WAVE_NUMBER","+22382803707"); ORANGE=os.getenv("ORANGE_NUMBER","+22382803707"); DB="digital_market.db"
CATS={"🎮 Jeux PS2":"PS2","🎮 Jeux PS3":"PS3","🎮 Jeux PS4":"PS4","🎮 Jeux PS5":"PS5","🎮 PSP":"PSP","🎮 PS Vita":"PS Vita","🎮 Nintendo":"Nintendo","💻 Jeux PC":"PC","📱 Jeux Android":"Android","🕹 Consoles":"Consoles","🎮 Manettes":"Manettes","🎧 Accessoires":"Accessoires","💳 Abonnements":"Abonnements"}
ADD_NAME,ADD_CAT,ADD_PRICE,ADD_DESC,ADD_DELIVERY=range(5)

def db():
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row;return c
def init_db():
 c=db();c.execute("CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,category TEXT,price INTEGER,description TEXT DEFAULT '',file_id TEXT DEFAULT '',link TEXT DEFAULT '',active INTEGER DEFAULT 1)")
 c.execute("CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,product_id INTEGER,status TEXT DEFAULT 'pending',payment_method TEXT DEFAULT '',proof_file_id TEXT DEFAULT '',created_at DATETIME DEFAULT CURRENT_TIMESTAMP)")
 c.commit();c.close()
def admin_user(u): return u and u.id==ADMIN_ID
def home(): return ReplyKeyboardMarkup([[a,b] for a,b in [["🎮 Jeux PS2","🎮 Jeux PS3"],["🎮 Jeux PS4","🎮 Jeux PS5"],["🎮 PSP","🎮 PS Vita"],["🎮 Nintendo","💻 Jeux PC"],["📱 Jeux Android","🕹 Consoles"],["🎮 Manettes","🎧 Accessoires"],["💳 Abonnements"],["🔎 Rechercher","🛒 Panier"],["📦 Mes commandes","📞 Support"]]],resize_keyboard=True)

async def start(u,c): await u.message.reply_text("🎮 DIGITAL MARKET GAMING\n\nBienvenue dans votre boutique.\nChoisissez une catégorie :",reply_markup=home())
async def admin(u,c):
 if not admin_user(u.effective_user): return await u.message.reply_text("❌ Accès refusé.")
 await u.message.reply_text("👨‍💼 PANNEAU ADMINISTRATEUR",reply_markup=ReplyKeyboardMarkup([["➕ Ajouter","📦 Produits"],["🛒 Commandes","📊 Statistiques"],["🏠 Accueil"]],resize_keyboard=True))
async def category(u,c):
 cat=CATS.get(u.message.text)
 if not cat:return
 d=db();rows=d.execute("SELECT * FROM products WHERE category=? AND active=1 ORDER BY id DESC",(cat,)).fetchall();d.close()
 if not rows:return await u.message.reply_text(f"📂 {cat}\n\nAucun produit disponible.")
 for p in rows: await u.message.reply_text(f"🎮 {p['name']}\n💰 {p['price']:,} FCFA\n📝 {p['description'] or '—'}",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🛒 Acheter",callback_data=f"buy:{p['id']}")]]))
async def buy(u,c):
 q=u.callback_query;await q.answer();pid=int(q.data.split(":")[1]);d=db();p=d.execute("SELECT * FROM products WHERE id=? AND active=1",(pid,)).fetchone();d.close()
 if not p:return await q.message.reply_text("❌ Produit indisponible.")
 await q.message.reply_text(f"🛒 {p['name']}\n💰 {p['price']:,} FCFA\n\nChoisissez le paiement :",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🟠 Orange Money",callback_data=f"pay:{pid}:orange"),InlineKeyboardButton("🔵 Wave",callback_data=f"pay:{pid}:wave")]]))
async def pay(u,c):
 q=u.callback_query;await q.answer();_,pid,method=q.data.split(":");d=db();p=d.execute("SELECT * FROM products WHERE id=?",(int(pid),)).fetchone();cur=d.execute("INSERT INTO orders(user_id,product_id,payment_method) VALUES(?,?,?)",(q.from_user.id,int(pid),method));oid=cur.lastrowid;d.commit();d.close()
 await q.message.reply_text(f"💳 COMMANDE #{oid}\nProduit : {p['name']}\nMontant : {p['price']:,} FCFA\nMoyen : {method.upper()}\nNuméro : {ORANGE if method=='orange' else WAVE}\n\nEffectuez le paiement puis envoyez la preuve ici.")
async def proof(u,c):
 if not (u.message.photo or u.message.document):return
 d=db();o=d.execute("SELECT * FROM orders WHERE user_id=? AND status='pending' ORDER BY id DESC LIMIT 1",(u.effective_user.id,)).fetchone()
 if not o:d.close();return
 fid=u.message.photo[-1].file_id if u.message.photo else u.message.document.file_id;d.execute("UPDATE orders SET proof_file_id=? WHERE id=?",(fid,o["id"]));p=d.execute("SELECT * FROM products WHERE id=?",(o["product_id"],)).fetchone();d.commit();d.close()
 await u.message.reply_text(f"✅ Preuve reçue pour la commande #{o['id']}.")
 await c.bot.send_message(ADMIN_ID,f"🔔 Preuve commande #{o['id']}\nProduit : {p['name']}\nClient : {u.effective_user.id}",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ Valider",callback_data=f"ok:{o['id']}"),InlineKeyboardButton("❌ Refuser",callback_data=f"no:{o['id']}")]]))
async def validate(u,c):
 q=u.callback_query
 if not admin_user(q.from_user):return await q.answer("Accès refusé",show_alert=True)
 act,oid=q.data.split(":");d=db();o=d.execute("SELECT * FROM orders WHERE id=?",(int(oid),)).fetchone();p=d.execute("SELECT * FROM products WHERE id=?",(o["product_id"],)).fetchone();status="paid" if act=="ok" else "rejected";d.execute("UPDATE orders SET status=? WHERE id=?",(status,int(oid)));d.commit();d.close()
 await q.edit_message_text(f"Commande #{oid} : {'VALIDÉE' if status=='paid' else 'REFUSÉE'}.")
 if status=="paid":
  if p["file_id"]: await c.bot.send_document(o["user_id"],p["file_id"],caption=f"✅ Commande #{oid}\n{p['name']}")
  elif p["link"]: await c.bot.send_message(o["user_id"],f"✅ Commande #{oid} validée.\nLien : {p['link']}")
  else: await c.bot.send_message(o["user_id"],f"✅ Commande #{oid} validée. Contactez le support.")
 else: await c.bot.send_message(o["user_id"],f"❌ Commande #{oid} refusée. Contactez le support.")
async def support(u,c): await u.message.reply_text(f"📞 SUPPORT\n\nWave : {WAVE}\nOrange Money : {ORANGE}")
async def myorders(u,c):
 d=db();r=d.execute("SELECT o.id,o.status,p.name,p.price FROM orders o JOIN products p ON p.id=o.product_id WHERE o.user_id=? ORDER BY o.id DESC",(u.effective_user.id,)).fetchall();d.close()
 await u.message.reply_text("📦 MES COMMANDES\n\n"+("\n".join(f"#{x['id']} — {x['name']} — {x['price']:,} FCFA — {x['status']}" for x in r) if r else "Aucune commande."))
async def products(u,c):
 if not admin_user(u.effective_user):return
 d=db();r=d.execute("SELECT id,name,category,price FROM products ORDER BY id DESC").fetchall();d.close();await u.message.reply_text("\n".join(f"#{x['id']} — {x['name']} — {x['category']} — {x['price']:,} FCFA" for x in r) if r else "Aucun produit.")
async def stats(u,c):
 if not admin_user(u.effective_user):return
 d=db();a=d.execute("SELECT COUNT(*) n FROM products").fetchone()["n"];b=d.execute("SELECT COUNT(*) n FROM orders").fetchone()["n"];e=d.execute("SELECT COUNT(*) n FROM orders WHERE status='paid'").fetchone()["n"];d.close();await u.message.reply_text(f"📊 STATISTIQUES\n\nProduits : {a}\nCommandes : {b}\nPayées : {e}")
async def add_start(u,c):
 if not admin_user(u.effective_user):return ConversationHandler.END
 await u.message.reply_text("➕ Nom du produit :");return ADD_NAME
async def add_name(u,c):c.user_data["name"]=u.message.text;await u.message.reply_text("Catégorie :");return ADD_CAT
async def add_cat(u,c):c.user_data["cat"]=u.message.text;await u.message.reply_text("Prix FCFA :");return ADD_PRICE
async def add_price(u,c):
 try:c.user_data["price"]=int(u.message.text.replace(" ","").replace(",",""))
 except ValueError:await u.message.reply_text("Prix invalide.");return ADD_PRICE
 await u.message.reply_text("Description :");return ADD_DESC
async def add_desc(u,c):c.user_data["desc"]=u.message.text;await u.message.reply_text("Envoie le fichier Telegram ou le lien :");return ADD_DELIVERY
async def add_delivery(u,c):
 d=c.user_data;fid="";link=""
 if u.message.document:fid=u.message.document.file_id
 elif u.message.video:fid=u.message.video.file_id
 elif u.message.text:link=u.message.text.strip()
 else:await u.message.reply_text("Envoie un fichier ou un lien.");return ADD_DELIVERY
 x=db();x.execute("INSERT INTO products(name,category,price,description,file_id,link) VALUES(?,?,?,?,?,?)",(d["name"],d["cat"],d["price"],d["desc"],fid,link));x.commit();x.close();c.user_data.clear();await u.message.reply_text("✅ Produit ajouté.");return ConversationHandler.END

def main():
 if not TOKEN:raise RuntimeError("BOT_TOKEN manquant")
 init_db();app=Application.builder().token(TOKEN).build()
 conv=ConversationHandler(entry_points=[MessageHandler(filters.Regex("^➕ Ajouter$"),add_start)],states={ADD_NAME:[MessageHandler(filters.TEXT&~filters.COMMAND,add_name)],ADD_CAT:[MessageHandler(filters.TEXT&~filters.COMMAND,add_cat)],ADD_PRICE:[MessageHandler(filters.TEXT&~filters.COMMAND,add_price)],ADD_DESC:[MessageHandler(filters.TEXT&~filters.COMMAND,add_desc)],ADD_DELIVERY:[MessageHandler(filters.Document.ALL|filters.VIDEO|(filters.TEXT&~filters.COMMAND),add_delivery)]},fallbacks=[CommandHandler("cancel",lambda u,c:ConversationHandler.END)])
 app.add_handler(CommandHandler("start",start));app.add_handler(CommandHandler("admin",admin));app.add_handler(conv);app.add_handler(CallbackQueryHandler(buy,pattern=r"^buy:\d+$"));app.add_handler(CallbackQueryHandler(pay,pattern=r"^pay:\d+:(orange|wave)$"));app.add_handler(CallbackQueryHandler(validate,pattern=r"^(ok|no):\d+$"));app.add_handler(MessageHandler(filters.PHOTO|filters.Document.ALL,proof));app.add_handler(MessageHandler(filters.Regex("^📦 Produits$"),products));app.add_handler(MessageHandler(filters.Regex("^📊 Statistiques$"),stats));app.add_handler(MessageHandler(filters.Regex("^📦 Mes commandes$"),myorders));app.add_handler(MessageHandler(filters.Regex("^📞 Support$"),support));app.add_handler(MessageHandler(filters.Regex("^🏠 Accueil$"),start));app.add_handler(MessageHandler(filters.TEXT&~filters.COMMAND,category));app.run_polling()
if __name__=="__main__":main()
