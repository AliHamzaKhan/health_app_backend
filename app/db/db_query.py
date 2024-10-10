import json
import logging
import uuid
from typing import Optional

import asyncpg
from dns.e164 import query

from app.api.tokens import generate_token
from app.db.database_connection import Database
from app.models import token_used
from app.models.ai_generated_text import AiGeneratedText
from app.models.ai_request_enum import AiRequestType
from app.models.data_process import DataProcess, DataProcessRequest
from app.models.doctor import DoctorRequest, Doctor
from app.models.hospital import Hospital, HospitalRequest
from app.models.rating import Rating, RatingRequest
from app.models.token_used import TokenUsed
from app.models.user_profile import UserProfile, UserProfileRequest


class DBQuery:

    def __init__(self, database: Database):
        self.database = database

    async def update_user_profile_with_token(self, token: str, user_id: str):
        """
        Updates the user's profile in the database with the generated token.
        """

        query = """
            UPDATE users
            SET token = $1
            where id = $2
            """

        try:
            await self.database.execute(query, token, user_id)
            logging.info(f"Token successfully added to user profile for user ID: {user_id}")


        except Exception as e:
            logging.error(f"An error occurred while updating the user profile: {e}")
            raise e












