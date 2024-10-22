import logging
import os
import uuid
from typing import Optional

from app import Database
from app.api.tokens import generate_token
from app.models.user_profile import UserProfile
from app.schema.app_schemas import CREATE_USER_SCHEMA, CHECK_USER_SCHEMA, INSERT_USER_SCHEMA
from app.service.profile_service import ProfileService


class LoginService:


    def __init__(self, database : Database):
        self.database = database


    # async def login(self, email : Optional[str], phone_no : Optional[str], user_type_id : Optional[int], fcm_token : Optional[str]):
    #     new_user_token = int(os.environ.get('NEW_USER_TOKENS'))
    #     if not phone_no and not email: raise ValueError("Either phone number or email must be provided.")
    #     profile : UserProfile = UserProfile(
    #         id = '',
    #         first_name='',
    #         last_name='',
    #         email=email,
    #         phone_no=phone_no,
    #         dob='',
    #         gender='',
    #         user_type_id=user_type_id,
    #         country='',
    #         city='',
    #         is_verified=True,
    #         package_id=7,
    #         usage=0,
    #         profile_image='',
    #     )
    #     try:
    #         await self.database.execute(CREATE_USER_SCHEMA)
    #         user = await self.database.fetch_one(CHECK_USER_SCHEMA, phone_no, email)
    #         if user:
    #             user_id = user['id']
    #             token = generate_token(user_id)
    #             # await ProfileService(self.database).save_user_profile(profile=profile)
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
    #             await self.database.execute(
    #                 INSERT_USER_SCHEMA, user_id, phone_no, email, new_user_token, user_type_id, token, fcm_token
    #             )
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