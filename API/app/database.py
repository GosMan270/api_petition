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


    async def add_other(self, text, status, ts, sentiment, category):
        await self.execute_query(
            "INSERT INTO complaints (text, status, timestamp, sentiment, category) VALUES (?, ?, ?, ?, ?)",
            (text, status, ts, sentiment, category)
        )


    async def get_complaints_filtered(self, status=None, since=None):
        query = "SELECT * FROM complaints WHERE 1=1"
        params = []
        if status:
            query += " AND status = ?"
            params.append(status)
        if since:
            query += " AND timestamp >= ?"
            params.append(since.isoformat())
        async with self.connection.execute(query, params) as cursor:
            rows = await cursor.fetchall()
            return rows


    async def update_status(self, complaint_id: int, status: str):
        await self.execute_query(
            "UPDATE complaints SET status = ? WHERE id = ?",
            (status, complaint_id)
        )




DATABASE = ProjectDatabase()