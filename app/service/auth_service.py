import logging
import os
import uuid
from typing import Optional
from app import Database
from app.api.tokens import generate_token
from app.models.user_profile import UserProfile
from app.schema.app_schemas import CREATE_USER_SCHEMA, CHECK_USER_SCHEMA, INSERT_USER_SCHEMA, UPDATE_USER_TOKEN_SCHEMA, \
    UPDATE_PROFILE_PACKAGE_ID_SCHEMA, CHECK_USER_BY_PHONE_SCHEMA, CHECK_USER_BY_EMAIL_SCHEMA
from app.service.profile_service import ProfileService


class AuthService:

    def __init__(self, database: Database):
        self.database = database

    # async def login(self, email: Optional[str], phone_no: Optional[str], user_type_id: Optional[int],
    #                 fcm_token: Optional[str]):
    #     new_user_token = int(os.environ.get('NEW_USER_TOKENS'))
    #     if not phone_no and not email: raise ValueError("Either phone number or email must be provided.")
    #     profile: UserProfile = UserProfile(
    #         id=None,  # Or you can generate this if needed
    #         first_name=None,
    #         last_name=None,
    #         email=email,
    #         phone_no=phone_no,
    #         dob=None,
    #         gender=None,
    #         user_type_id=user_type_id,
    #         country=None,
    #         city=None,
    #         is_verified=True,
    #         package_id=7,
    #         total_usage=0.0,
    #         profile_image=None,
    #     )
    #     try:
    #         await self.database.execute(CREATE_USER_SCHEMA)
    #         user = await self.database.fetch_one(CHECK_USER_SCHEMA, phone_no, email)
    #         if user:
    #             user_id = user['id']
    #             token = generate_token(user_id)
    #             await self.update_user_token(user_id, token)
    #
    #             user_data = dict(user)  # Convert the asyncpg.Record to a regular dictionary
    #             user_data['token'] = token
    #
    #             print(type(user))
    #             print(f"Returning existing user data: user_id={user_id}, token={token}")
    #             return {
    #                 'user': user,
    #                 'isNew': False
    #             }
    #         else:
    #             if user_type_id is None: raise ValueError("user_type_id must be provided for new users.")
    #             user_id = str(uuid.uuid4())
    #             token = generate_token(user_id)
    #             profile.id = user_id
    #             print('profile.id', profile.id)
    #             await self.database.execute(INSERT_USER_SCHEMA, user_id, phone_no, email, new_user_token, user_type_id,
    #                                         token, fcm_token)
    #             user = await self.database.fetch_one(CHECK_USER_SCHEMA, phone_no, email)
    #             await ProfileService(self.database).save_user_profile(profile=profile)
    #             print(
    #                 f"Returning new user data: user_id={user_id}, token={token}, user_type={user_type_id}, new_user_token={new_user_token}")
    #             return {
    #                 'user': user,
    #                 'isNew': True
    #             }
    #
    #     except Exception as e:
    #         logging.error(f"An error occurred during login/signup: {e}")
    #         raise RuntimeError("An error occurred. Please try again later.") from e


    async def login(self, email: Optional[str], phone_no: Optional[str], user_type_id: Optional[int], fcm_token: Optional[str]):
        new_user_token = int(os.environ.get('NEW_USER_TOKENS'))
        if not phone_no and not email:
            raise ValueError("Either phone number or email must be provided.")

        await self.database.execute(CREATE_USER_SCHEMA)

        if phone_no:
            user = await self.database.fetch_one(CHECK_USER_BY_PHONE_SCHEMA, phone_no)
        else:
            user = await self.database.fetch_one(CHECK_USER_BY_EMAIL_SCHEMA, email)

        if user:
            return await self.handle_existing_user(user)
        else:
            return await self.handle_new_user(email, phone_no, user_type_id, fcm_token, new_user_token)

    async def handle_existing_user(self, user):
        user_id = user['id']
        token = generate_token(user_id)
        await self.update_user_token(user_id, token)

        user_data = dict(user)
        user_data['token'] = token

        logging.info(f"Returning existing user data: user_id={user_id}, token={token}")
        return {
            'user': user_data,
            'isNew': False
        }

    async def handle_new_user(self, email, phone_no, user_type_id, fcm_token, new_user_token):
        if user_type_id is None:
            raise ValueError("user_type_id must be provided for new users.")

        user_id = str(uuid.uuid4())
        token = generate_token(user_id)

        profile = UserProfile(
            id=user_id,
            first_name=None,
            last_name=None,
            email=email,
            phone_no=phone_no,
            dob=None,
            gender=None,
            user_type_id=user_type_id,
            country=None,
            city=None,
            is_verified=True,
            package_id=7,
            total_usage=0.0,
            profile_image=None,
        )

        try:
            await self.database.execute(INSERT_USER_SCHEMA,user_id, phone_no, email, new_user_token, user_type_id,token, fcm_token)
            await ProfileService(self.database).save_user_profile(profile=profile)
            user = await self.database.fetch_one(CHECK_USER_BY_PHONE_SCHEMA,phone_no)
            logging.info(
                f"Returning new user data: user_id={user_id}, token={token}, user_type={user_type_id}, new_user_token={new_user_token}")
            return {
                'user': user,
                'isNew': True
            }

        except Exception as e:
            logging.error(f"An error occurred during login/signup: {e}")
            raise RuntimeError("An error occurred. Please try again later.") from e



    async def get_user_by_id(self, user_id: str):
        search_query = """
               SELECT * FROM users WHERE id = $1
               """

        try:
            user = await self.database.fetchrow(search_query, user_id)
            if user:
                return user
            else:
                return None
        except Exception as e:
            logging.error(f"Failed to get_user_by_id {user_id}: {e}")
            return None

    async def get_user_types(self):

        get_query = "SELECT user_type_id, user_type_name FROM user_types;"
        try:
            data = await self.database.fetch(get_query)
            print(f'get_user_types {data}')
            if not data:
                return []
            return [{"user_type_id": record["user_type_id"], "user_type_name": record["user_type_name"]} for record in
                    data]
        except Exception as e:
            logging.error(f"Failed to get_user_types: {e}")
            return []

    async def get_packages(self):
        try:
            get_query = "SELECT * FROM packages;"
            data = await self.database.fetch(get_query)
            print(f'get_packages {data}')

            if not data:
                return []

            # Return a list of dictionaries for each record in data
            return [dict(record) for record in data]
        except Exception as e:
            logging.error(f"Failed to get get_packages: {e}")
            return []

    async def update_user_token(self, user_id: str, token: str):
        try:
            await self.database.execute(UPDATE_USER_TOKEN_SCHEMA, token, user_id)
            print(f"Token updated successfully for user_id: {user_id}")
        except Exception as e:
            logging.error(f"Failed to update user token for user_id {user_id}: {e}")
            raise Exception("Failed to update user token")

    async def update_user_package(self, user_id: str, package_id: int):
        try:
            await self.database.execute(UPDATE_PROFILE_PACKAGE_ID_SCHEMA, package_id, user_id)
            print(f"update_user_package updated successfully for package_id : {package_id} , user_id: {user_id}")
        except Exception as e:
            logging.error(f"Failed to update user token for package_id : {package_id} , user_id {user_id}: {e}")
            raise Exception("Failed to update update_user_package")
