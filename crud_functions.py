import aiosqlite

async def initiate_db():
    """Создает таблицы Products и Users, если они еще не созданы."""
    # Создаем базу данных для продуктов
    async with aiosqlite.connect('products.db') as conn:
        cursor = await conn.cursor()

        # Создание таблицы Products
        await cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS Products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                price INTEGER NOT NULL
            )
        ''')
        await conn.commit()

    # Создаем базу данных для пользователей
    async with aiosqlite.connect('initiate.db') as conn:
        cursor = await conn.cursor()

        # Создание таблицы Users
        await cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER NOT NULL,
                balance INTEGER NOT NULL DEFAULT 1000
            )
        ''')
        await conn.commit()

async def get_all_products():
    """Возвращает все записи из таблицы Products."""
    async with aiosqlite.connect('products.db') as conn:
        cursor = await conn.cursor()
        await cursor.execute('SELECT title, description, price FROM Products')
        products = await cursor.fetchall()
        return products

async def insert_sample_data():
    """Заполняет таблицу Products примерными данными."""
    async with aiosqlite.connect('products.db') as conn:
        cursor = await conn.cursor()

        # Проверяем, есть ли уже данные в таблице
        await cursor.execute('SELECT COUNT(*) FROM Products')
        count = await cursor.fetchone()

        if count[0] == 0:
            sample_products = [
                ('CodliverOil', 'Кодливерное масло, полезно для здоровья.', 500),
                ('PapayaLeaf', 'Листья папайи, хороши для пищеварения.', 300),
                ('VitaminCOriginal', 'Оригинальный витамин C, укрепляет иммунитет.', 400),
                ('CranberryExtract', 'Экстракт клюквы, полезен для мочевыводящих путей.', 350),
                ('Ginseng', 'Женьшень, повышает жизненную силу.', 600),
                ('SeleniumAdvanced', 'Улучшенный селен, поддерживает здоровье.', 450),
            ]
            await cursor.executemany('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)', sample_products)
            await conn.commit()

async def add_user(username, email, age):
    """Добавляет пользователя в таблицу Users с балансом 1000."""
    async with aiosqlite.connect('initiate.db') as conn:
        cursor = await conn.cursor()
        await cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                             (username, email, age, 1000))
        await conn.commit()

async def is_included(username):
    """Проверяет, существует ли пользователь с данным именем."""
    async with aiosqlite.connect('initiate.db') as conn:
        cursor = await conn.cursor()
        await cursor.execute('SELECT COUNT(*) FROM Users WHERE username = ?', (username,))
        count = await cursor.fetchone()
        return count[0] > 0

async def register_user(username, email, age):
    """Регистрация пользователя в базе данных."""
    async with aiosqlite.connect('initiate.db') as conn:
        cursor = await conn.cursor()
        # Вставка данных о пользователе
        await cursor.execute('INSERT INTO Users (username, email, age) VALUES (?, ?, ?)', (username, email, age))
        await conn.commit()
