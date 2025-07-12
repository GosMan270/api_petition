"""
Async database layer using aiosqlite for complaints management.
"""

import aiosqlite


class Database:
    """
    Base async DB class with simple CRUD methods.
    """
    def __init__(self):
        self.connection: aiosqlite.Connection = None
        self._last_row_id: int = 0

    async def open_connection(self, db_path: str):
        """Open connection to DB."""
        self.connection = await aiosqlite.connect(db_path)
        await self.connection.execute("PRAGMA foreign_keys = ON;")

    async def close_connection(self):
        """Close DB connection if exists."""
        if self.connection:
            await self.connection.close()
            self.connection = None

    async def execute_query(self, query: str, params: tuple = None) -> None:
        """Execute a DB query (no return), keep last insert id."""
        if not self.connection:
            raise RuntimeError("Database connection is not open!")
        async with self.connection.execute(query, params or ()) as cursor:
            self._last_row_id = cursor.lastrowid
        await self.connection.commit()

    async def execute_get_query(self, query: str, params: tuple = None):
        """Execute a DB query and return all fetched rows."""
        if not self.connection:
            raise RuntimeError("Database connection is not open!")
        async with self.connection.execute(query, params or ()) as cursor:
            return await cursor.fetchall()

    @property
    def last_id(self):
        """Return last inserted row id."""
        return self._last_row_id


class ProjectDatabase(Database):
    """
    Project-specific logic for complaints table.
    """
    async def add_other(self, text, status, ts, sentiment, category):
        """
        Add new complaint to the DB.
        Args:
            text: complaint text
            status: complaint status
            ts: timestamp
            sentiment: sentiment label
            category: category label
        """
        await self.execute_query(
            "INSERT INTO complaints (text, status, timestamp, sentiment, category) VALUES (?, ?, ?, ?, ?)",
            (text, status, ts, sentiment, category)
        )

    async def get_complaints_filtered(self, status=None, since=None):
        """
        Get complaints list by (optional) status and since-timestamp filter.
        """
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
        """
        Update complaint status by id.
        """
        await self.execute_query(
            "UPDATE complaints SET status = ? WHERE id = ?",
            (status, complaint_id)
        )


DATABASE = ProjectDatabase()