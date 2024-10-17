import logging
import os
import uuid
from typing import Optional, Dict

from app import Database
from app.api.tokens import generate_token


class AuthService:

    def __init__(self, database: Database):
        self.database = database

    async def login(self, user_type_id: Optional[int] = None, phone_number: Optional[str] = None,
                    email: Optional[str] = None, fcm_token: Optional[str] = None):
        """
        Authenticates a user by either phone number or email.
        If the user exists, return user ID and token.
        If the user does not exist, create a new user, generate a token, and return the data.
        """


        new_user_token = int(os.environ.get('NEW_USER_TOKENS'))

        if not phone_number and not email:
            raise ValueError("Either phone number or email must be provided.")

        # Ensure the 'users' table exists
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(36) PRIMARY KEY,
            phone_no VARCHAR(15),
            email VARCHAR(255),
            ai_tokens INTEGER,
            user_type_id INTEGER,
            token VARCHAR(255),
            fcm_token VARCHAR(255)  
        )
        """

        try:
            await self.database.execute(create_table_query)

            check_user_query = """
            SELECT * FROM users WHERE phone_no = COALESCE($1, phone_no) OR email = COALESCE($2, email)
            """

            # Fetch user based on phone number or email
            user = await self.database.fetch_one(check_user_query, phone_number, email)

            print(f"Fetched user: {user}")
            if user:
                # User exists
                user_id = user['id']
                token = generate_token(user_id)
                print(type(user))# Generate a new token for the existing user
                # user['token'] = token
                print(f"Returning existing user data: user_id={user_id}, token={token}")
                return {
                    'user' : user,
                    'isNew' : False
                }
            else:
                # User does not exist, create a new user
                if user_type_id is None:
                    raise ValueError("user_type_id must be provided for new users.")

                user_id = str(uuid.uuid4())  # Generate a unique UUID for the user
                token = generate_token(user_id)  # Generate a token for the new user

                # Insert new user into the database
                insert_user_query = """
                    INSERT INTO users (id, phone_no, email, ai_tokens, user_type_id, token, fcm_token)
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
                    """
                await self.database.execute(
                    insert_user_query, user_id, phone_number, email, new_user_token, user_type_id, token, fcm_token
                )

                print(
                    f"Returning new user data: user_id={user_id}, token={token}, user_type={user_type_id}, new_user_token={new_user_token}")
                return {
                    'user': user,
                    'isNew': True
                }

        except Exception as e:
            logging.error(f"An error occurred during login/signup: {e}")
            raise RuntimeError("An error occurred. Please try again later.") from e

    async def get_user(self, phone_number: Optional[str] = None, email: Optional[str] = None):
        if not phone_number and not email:
            raise ValueError("Either phone number or email must be provided.")

        search_query = """
        SELECT * FROM users where phone_no = COALESCE($1, phone_no) OR email = COALESCE($2, email)
        """

        user = await self.database.fetch_one(search_query, phone_number, email)
        if user:
            _id = user.get('id')
            phone_no = user.get('phone_no')
            email = user.get('email')
            token = user.get('token')
            user_type_id = user.get('user_type_id')

            return {
                'user_id': _id,
                'phone_no': phone_no,
                'email': email,
                'token': token,
                'user_type': user_type_id,
            }

        return {
            'user_id': '',
            'phone_no': '',
            'email': '',
            'token': '',
            'user_type': '',
        }

    async def get_user_types(self):
        get_query = "SELECT user_type_id, user_type_name FROM user_types;"
        data = await self.database.fetch(get_query)
        print(f'get_user_types {data}')
        if not data:
            return []

        return [{"user_type_id": record["user_type_id"], "user_type_name": record["user_type_name"]} for record in data]

    async def get_packages(self):
        get_query = "SELECT * FROM packages;"
        data = await self.database.fetch(get_query)
        print(f'get_packages {data}')

        if not data:
            return []

        # Return a list of dictionaries for each record in data
        return [dict(record) for record in data]
