import logging, asyncpg


class Database:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.connection = None


    async def connect(self):
        """Connect to the PostgreSQL database."""
        try:
            self.connection = await asyncpg.connect(self.database_url)
            print("Database connection established.")
            logging.info("Database connection established.")
        except asyncpg.exceptions.PostgresError as e:
            print(f"Failed to connect to the database: {e}")
            logging.error(f"Failed to connect to the database: {e}")
            raise

    async def close(self):
        """Close the connection to the database."""
        if self.connection:
            try:
                await self.connection.close()
                logging.info("Database connection closed.")
            except asyncpg.exceptions.PostgresError as e:
                logging.error(f"Failed to close the database connection: {e}")

    def get_connection(self):
        """Return the current database connection."""
        if self.connection is None:
            logging.warning("Attempted to use a database connection that is not established.")
            raise ConnectionError("Database connection is not established.")
        return self.connection

    async def execute(self, query: str, *args):
        """Execute a query against the database."""
        if self.connection is None:
            raise ConnectionError("Database connection is not established.")
        try:
            async with self.connection.transaction():
                return await self.connection.execute(query, *args)
        except asyncpg.exceptions.PostgresError as e:
            logging.error(f"Failed to execute query: {e}")
            raise

    async def fetch(self, query: str, *args):
        """Fetch results from the database."""
        if self.connection is None:
            raise ConnectionError("Database connection is not established.")
        try:
            return await self.connection.fetch(query, *args)
        except asyncpg.exceptions.PostgresError as e:
            logging.error(f"Failed to fetch data: {e}")
            raise

    async def fetchrow(self, query: str, *args):
        """Fetch a single row from the database."""
        if self.connection is None:
            raise ConnectionError("Database connection is not established.")
        try:
            return await self.connection.fetchrow(query, *args)
        except asyncpg.exceptions.PostgresError as e:
            logging.error(f"Failed to fetch row: {e}")
            raise

    async def fetchval(self, query: str, *args):
        """Fetch a single value from the database."""
        if self.connection is None:
            raise ConnectionError("Database connection is not established.")
        try:
            return await self.connection.fetchval(query, *args)
        except asyncpg.exceptions.PostgresError as e:
            logging.error(f"Failed to fetch value: {e}")
            raise

    async def fetch_one(self, query: str, *args):
        try:
            row = await self.connection.fetchrow(query, *args)
            print(row)
            if row:
                return row
            return None
        except Exception as e:
            logging.error(f"An error occurred during fetch_one: {e}")
            raise e