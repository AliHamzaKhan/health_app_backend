import logging
import uuid

import asyncpg

from app import Database
from app.models.user_profile import UserProfileRequest, UserProfile
from app.service.auth_service import AuthService
import app.service.initialize_service as service


class ProfileService:

    def __init__(self, database: Database):
        self.database = database


    async def get_user_profile(self, email: str):
        """Fetch a user profile by email."""
        query = """
    SELECT * FROM profiles WHERE id = $1;
    """
        try:

            profile_row = await self.database.fetchrow(query, email)
            if profile_row:
                return {column: value for column, value in profile_row.items()}  # Convert to dictionary
            else:
                logging.warning(f"No profile found for email: {email}")
                return None
        except asyncpg.exceptions.PostgresError as e:
            logging.error(f"Failed to fetch user profile: {e}")
            raise

    async def save_user_profile(self, profile: UserProfile):
        """Insert or update a user profile in the database."""
        # id = str(uuid.uuid4())

        user = await service.auth_service.get_user(phone_number='8327487234')
        print(f'user {user}')

        token = ''  # get from user profile if exists
        create_table_query = """
        CREATE TABLE IF NOT EXISTS profiles (
            id VARCHAR(250),
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            email VARCHAR(100) UNIQUE,
            phone_no VARCHAR(15),
            dob VARCHAR(50),
            country VARCHAR(50),
            city VARCHAR(50),
            gender CHAR(10),
            profile_image TEXT,
            is_verified BOOLEAN,
            package_id INT,
            usage FLOAT,
            user_type_id INT,
            token VARCHAR(250)
        );
    """
        await self.database.execute(create_table_query)  # Create the table if it doesn't exist

        insert_query = """
    INSERT INTO profiles (first_name, last_name, email, phone_no, dob, country,city ,gender, profile_image, is_verified, package_id, usage, user_type_id, token)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
    ON CONFLICT (phone_no) DO UPDATE SET
        id = id,
        first_name = EXCLUDED.first_name,
        last_name = EXCLUDED.last_name,
        phone_no = EXCLUDED.phone_no,
        dob = EXCLUDED.dob,
        country = EXCLUDED.country,
        city = EXCLUDED.city,
        gender = EXCLUDED.gender,
        profile_image = EXCLUDED.profile_image,
        is_verified = EXCLUDED.is_verified,
        package_id = EXCLUDED.package_id,
        usage = EXCLUDED.usage,
        user_type_id = EXCLUDED.user_type_id,
        token = EXCLUDED.token;
    """

        data_to_insert = (
            profile.first_name,
            profile.last_name, profile.email,
            profile.phone_no, profile.dob, profile.country, profile.city, profile.gender,
            profile.profile_image, profile.is_verified, profile.package_id,
            profile.usage, profile.user_type_id, token
        )

        await self.database.execute(insert_query, *data_to_insert)