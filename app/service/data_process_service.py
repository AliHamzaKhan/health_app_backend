import json
import uuid
from datetime import datetime

from app import Database
from app.models.ai_generated_text import AiGeneratedText
from app.models.ai_request_enum import AiRequestType
from app.models.data_process import DataProcessRequest, DataProcess


class DataProcessService:

    def __init__(self, database: Database):
        self.database = database

    async def save_data_process(self, data_process: DataProcessRequest) -> str:
        create_table_query = """
            CREATE TABLE IF NOT EXISTS data_process (
                id VARCHAR(255) PRIMARY KEY,
                user_id VARCHAR(255),
                prompt TEXT,
                image_url TEXT,
                token_used INTEGER,
                ai_generated_text JSONB,
                request_type VARCHAR(50),
                created_at TIMESTAMP DEFAULT NOW()
            );
        """

        insert_query = """
            INSERT INTO data_process (id, user_id, prompt, image_url, token_used, ai_generated_text, request_type, created_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            ON CONFLICT (id) DO UPDATE SET
                user_id = EXCLUDED.user_id,
                prompt = EXCLUDED.prompt,
                image_url = EXCLUDED.image_url,
                token_used = EXCLUDED.token_used,
                ai_generated_text = EXCLUDED.ai_generated_text,
                request_type = EXCLUDED.request_type;
        """

        new_id = str(uuid.uuid4())  # Generate a new UUID
        created_at = datetime.utcnow()  # Get the current timestamp

        data_to_insert = (
            new_id,
            data_process.user_id,  # Ensure correct field name
            data_process.prompt,
            data_process.image_url,
            data_process.token_used,
            data_process.ai_generated_text.json(),
            data_process.request_type.value,
            created_at
        )

        try:
            await self.database.execute(create_table_query)
            await self.database.execute(insert_query, *data_to_insert)
            print("DataProcess inserted or updated successfully!")
            return new_id

        except Exception as e:
            print(f"An error occurred while saving DataProcess: {e}")
            raise

    async def get_data_process(self, user_id: str, request_type: AiRequestType = None):
        query = """
            SELECT id, user_id, prompt, image_url, ai_generated_text, request_type, token_used, created_at
            FROM data_process 
            WHERE user_id = $1
        """
        params = [user_id]

        if request_type is not None:
            query += " AND request_type = $2"
            params.append(request_type.value)  # Ensure enum value is passed

        try:
            data_processes = await self.database.fetch(query, *params)

            if not data_processes:
                return []

            data_process_list = [
                DataProcess(
                    id=row["id"],
                    user_id=row["user_id"],
                    prompt=row["prompt"],
                    image_url=row["image_url"],
                    token_used=row["token_used"],
                    ai_generated_text=AiGeneratedText(**json.loads(row["ai_generated_text"])),
                    request_type=AiRequestType(row["request_type"]),
                    created_at=row["created_at"]
                )
                for row in data_processes
            ]

            return data_process_list

        except Exception as e:
            print(f"An error occurred while fetching DataProcess: {e}")
            raise

    async def get_single_data_process(self, data_process_id : str):
        query = """
                   SELECT id, user_id, prompt, image_url, ai_generated_text, request_type, token_used, created_at
                   FROM data_process 
                   WHERE id = $1
               """
        try:
            process_data = await self.database.fetch_one(query, data_process_id)
            print(process_data)
            if process_data is None:
                print(f"No data process found for ID: {data_process_id}")
                return None  # Return None if no data is found

            return DataProcess(
                id=process_data["id"],
                user_id=process_data["user_id"],
                prompt=process_data["prompt"],
                image_url=process_data["image_url"],
                token_used=process_data["token_used"],
                ai_generated_text=AiGeneratedText(**json.loads(process_data["ai_generated_text"])),
                request_type=AiRequestType(process_data["request_type"]),
                created_at=process_data["created_at"]
            )

        except Exception as e:
            print(f"An error occurred while fetching DataProcess: {e}")
            raise