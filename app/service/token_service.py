import logging
import time
from datetime import datetime
from typing import Optional
from uuid import uuid4

from app import Database


class TokenService:
    def __init__(self, database: Database):
        self.database = database

    async def save_used_token(self, token_used: int, user_id: str, process_id: int):
        """
        Saves or updates the used token for a user and data process.
        Creates the table if it doesn't exist.
        """
        create_table_query = """
            CREATE TABLE IF NOT EXISTS used_token (
                id VARCHAR(250) PRIMARY KEY,
                user_id VARCHAR(250) NOT NULL,
                data_process_id VARCHAR(250) NOT NULL,
                token_used INT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """

        await self.database.execute(create_table_query)

        insert_query = """
                    INSERT INTO used_token (id, user_id, data_process_id, token_used, created_at) 
                    VALUES ($1, $2, $3, $4, $5)
                    ON CONFLICT (id) DO UPDATE SET
                        user_id = EXCLUDED.user_id,
                        data_process_id = EXCLUDED.data_process_id,
                        token_used = EXCLUDED.token_used;
                    -- Notice `created_at` is not updated in case of conflict
                """

        # Extract values from the dictionary
        id = str(uuid4())  # Generate UUID for id if not provided
        created_at = datetime.utcnow()

        data_to_insert = (
            id,
            user_id,
            process_id,
            token_used,
            created_at
        )
        print(data_to_insert)

        try:
            await self.database.execute(insert_query, *data_to_insert)
            logging.info(
                f"Successfully saved/updated token usage for user ID: {user_id}, data process ID: {process_id}")
        except Exception as e:
            logging.error(f"An error occurred while saving the used token: {e}")
            raise e


    async def get_used_token(self, user_id: str, data_process_id: Optional[str] = None):
        """
        Retrieves the used token for a given user and optionally for a specific data process.
        """
        base_query = """
            SELECT id, user_id, data_process_id, token_used , created_at
            FROM used_token 
            WHERE user_id = $1
        """
        params = [user_id]

        if data_process_id:
            base_query += " AND data_process_id = $2"
            params.append(data_process_id)

        try:
            tokens = await self.database.fetch(base_query, *params)
            if tokens:
                logging.info(f"Retrieved {len(tokens)} tokens for user ID: {user_id}")
            else:
                logging.info(f"No tokens found for user ID: {user_id}")
            return tokens
        except Exception as e:

            logging.error(f"An error occurred while fetching the used tokens: {e}")
            raise e

    async def get_used_token_by_id(self, token_id: str):

        find_query = """
        SELECT id, user_id, data_process_id, token_used
        FROM used_token
        WHERE id = $1
        """

        try:
            tokens = await self.database.fetch_one(find_query, token_id)
            if tokens:
                return tokens

            else:
                logging.info(f"No tokens found for user ID: {token_id}")

        except Exception as e:
            logging.error(f"An error occurred while fetching the used tokens: {e}")
            raise e
