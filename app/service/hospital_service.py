import logging
import uuid
from typing import Optional

from app import Database
from app.models.hospital import Hospital, HospitalRequest
from app.schema.app_schemas import CREATE_HOSPITAL_SCHEME, INSERT_HOSPITAL_SCHEMA, FIND_HOSPITAL_IN_CITY_SCHEMA, \
    FIND_HOSPITAL_VALUES_SCHEMA, FIND_HOSPITALS_SCHEMA
from app.service.department_service import DepartmentService
from app.service.profile_service import ProfileService


class HospitalService:

    def __init__(self, database: Database):
        self.database = database

    async def get_hospitals(self, user_id: str, city: Optional[str], lat_lng: Optional[str]):
        """
        Retrieve hospitals near the user based on the city in the user's profile.
        """
        # if city:
        #     profile = ProfileService(self.database)
        #     user_profile = await profile.get_user_profile(user_id)
        #     if not user_profile:
        #         logging.error(f"User profile not found for user_id: {user_id}")
        #     else:
        #         city = user_profile.get("city")
        #     return []
        #
        #
        # if not city:
        #     logging.warning(f"No city found in user profile for user_id: {user_id}")
        #     return []

        try:
            hospitals_data = await self.database.fetch(FIND_HOSPITALS_SCHEMA)
            if not hospitals_data:
                return []

            print(hospitals_data)
            return hospitals_data



        except Exception as e:
            logging.error(f"An error occurred while fetching hospitals for user_id {user_id} in city {city}: {e}")
            raise e

    async def add_hospital(self, hospital: HospitalRequest):
        """
        Add a new hospital or update an existing hospital by email (upsert operation).
        """

        hospital_id = str(uuid.uuid4())
        print('hospital_id:', hospital_id)
        await self.database.execute(CREATE_HOSPITAL_SCHEME)
        try:
            data_to_insert = (
                hospital_id,
                hospital.name,
                hospital.address,
                hospital.phone_number,
                hospital.email,
                hospital.website,
                hospital.type,
                hospital.latlng,
                hospital.img,
                hospital.staff_count,
            )
            await self.database.execute(INSERT_HOSPITAL_SCHEMA, *data_to_insert)
            await DepartmentService(self.database).set_hospital_department(department_ids=hospital.departments,
                                                                           hospital_id=hospital_id)
            logging.info(f"Hospital '{hospital.name}' successfully added or updated.")
        except Exception as e:
            logging.error(f"Failed to add/update hospital '{hospital.name}': {e}")
            raise e

    async def get_hospital_values(self):
        try:
            data = await self.database.fetch(FIND_HOSPITAL_VALUES_SCHEMA)
            print(data)
            return data

        except Exception as e:
            logging.error(f"An error occurred while fetching get_hospital_values {e}")
            raise e
