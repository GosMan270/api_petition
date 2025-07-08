import aiosqlite


class Database:
    def __init__(self):
        self.connection: aiosqlite.Connection = None
        self._last_row_id: int = 0

    async def open_connection(self, db_path: str):
        self.connection = await aiosqlite.connect(db_path)
        await self.connection.execute("PRAGMA foreign_keys = ON;")

    async def close_connection(self):
        if self.connection:
            await self.connection.close()
            self.connection = None

    async def execute_query(self, query: str, params: tuple = None) -> None:
        if not self.connection:
            raise RuntimeError("Database connection is not open!")
        async with self.connection.execute(query, params or ()) as cursor:
            self._last_row_id = cursor.lastrowid
        await self.connection.commit()

    async def execute_get_query(self, query: str, params: tuple = None):
        if not self.connection:
            raise RuntimeError("Database connection is not open!")
        async with self.connection.execute(query, params or ()) as cursor:
            return await cursor.fetchall()

    @property
    def last_id(self):
        return self._last_row_id


class ProjectDatabase(Database):
    def __init__(self):
        super().__init__()

    async def get_or_create_user(self, tg_id: int, create_if_not_found: bool = True):
        rows = await self.execute_get_query("SELECT * FROM users WHERE id = ?", (tg_id,))
        if not rows and create_if_not_found:
            await self.execute_query("INSERT INTO users(id) VALUES (?)", (tg_id,))
            rows = await self.execute_get_query("SELECT * FROM users WHERE id = ?", (tg_id,))
        return rows[0] if rows else None

    async def get_subscriptions(self):
        return await self.execute_get_query("SELECT * FROM subscriptions")

    async def add_other(self, text, status, ts, sentiment, category):
        print('add_other')
        await self.execute_query(
            "INSERT INTO complaints (text, status, timestamp, sentiment, category) VALUES (?, ?, ?, ?, ?)",
            (text, status, ts, sentiment, category)
        )


DATABASE = ProjectDatabase()