import logging
import uuid
import asyncpg
from app import Database
from app.models.user_profile import UserProfileRequest, UserProfile
from app.schema.app_schemas import CREATE_PROFILE_SCHEMA, INSERT_PROFILE_SCHEMA, FIND_PROFILE_ID_SCHEMA


class ProfileService:

    def __init__(self, database: Database):
        self.database = database

    async def get_user_profile(self, user_id: str):

        try:
            profile_row = await self.database.fetchrow(FIND_PROFILE_ID_SCHEMA, user_id)
            if profile_row:
                return {column: value for column, value in profile_row.items()}  # Convert to dictionary
            else:

                logging.warning(f"No profile found for id: {user_id}")
                return None
        except asyncpg.exceptions.PostgresError as e:
            logging.error(f"Failed to fetch user profile: {e}")
            raise

    async def save_user_profile(self, profile: UserProfile):

        print('save_user_profile')
        try:
           await self.database.execute(CREATE_PROFILE_SCHEMA)
           data_to_insert = (
               profile.id,
               profile.first_name,
               profile.last_name, profile.email,
               profile.phone_no, profile.dob, profile.country, profile.city, profile.gender,
               profile.profile_image, profile.is_verified, profile.package_id,
               profile.total_usage, profile.user_type_id
           )

           await self.database.execute(INSERT_PROFILE_SCHEMA, *data_to_insert)

        except asyncpg.exceptions.PostgresError as e:
            logging.error(f"Failed to save_user_profile: {e}")
            raise
