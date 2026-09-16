"""
Base de données SQLite (via aiosqlite) : produits et commandes.
"""

import aiosqlite
from config import DB_PATH

CREATE_PRODUCTS_TABLE = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL,
    active INTEGER DEFAULT 1
);
"""

CREATE_ORDERS_TABLE = """
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    username TEXT,
    product_id INTEGER NOT NULL,
    status TEXT DEFAULT 'en_attente',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products (id)
);
"""


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(CREATE_PRODUCTS_TABLE)
        await db.execute(CREATE_ORDERS_TABLE)
        await db.commit()


async def get_categories_with_products():
    """Retourne les catégories qui ont au moins un produit actif."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT DISTINCT category FROM products WHERE active = 1"
        )
        rows = await cursor.fetchall()
        return [row[0] for row in rows]


async def get_products_by_category(category: str):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT id, name, price FROM products WHERE category = ? AND active = 1",
            (category,),
        )
        return await cursor.fetchall()


async def get_product(product_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT id, category, name, description, price FROM products WHERE id = ?",
            (product_id,),
        )
        return await cursor.fetchone()


async def add_product(category: str, name: str, description: str, price: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO products (category, name, description, price) VALUES (?, ?, ?, ?)",
            (category, name, description, price),
        )
        await db.commit()


async def remove_product(product_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE products SET active = 0 WHERE id = ?", (product_id,)
        )
        await db.commit()


async def create_order(user_id: int, username: str, product_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO orders (user_id, username, product_id) VALUES (?, ?, ?)",
            (user_id, username, product_id),
        )
        await db.commit()
        return cursor.lastrowid


async def set_order_status(order_id: int, status: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE orders SET status = ? WHERE id = ?", (status, order_id)
        )
        await db.commit()


async def get_order(order_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT id, user_id, username, product_id, status FROM orders WHERE id = ?",
            (order_id,),
        )
        return await cursor.fetchone()


async def get_user_orders(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """
            SELECT orders.id, products.name, orders.status, orders.created_at
            FROM orders
            JOIN products ON orders.product_id = products.id
            WHERE orders.user_id = ?
            ORDER BY orders.created_at DESC
            """,
            (user_id,),
        )
        return await cursor.fetchall()
