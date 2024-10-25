import logging
from typing import List

from app import Database
from app.schema.app_schemas import FIND_MEDICAL_SPECIALITIES_SCHEMA, CREATE_MEDICAL_SPECIALITIES_SCHEMA, \
    INSERT_MEDICAL_SPECIALITIES_SCHEMA, FIND_MEDICAL_SPECIALITIES_NAME_SCHEMA


class MedicalSpecialitiesService:

    def __init__(self, database : Database):
        self.database = database


    async def get_medical_specialities(self):
        try:
            data = await self.database.fetch(FIND_MEDICAL_SPECIALITIES_SCHEMA)
            if data:
                return data
            else:
                return None
        except Exception as e:
            logging.error(f"Failed to get_medical_specialities DepartmentService : {e}")
            raise e

    async def get_medical_specialities_names(self):
        try:
            data = await self.database.fetch(FIND_MEDICAL_SPECIALITIES_NAME_SCHEMA)
            if data:
                return data
            else:
                return None
        except Exception as e:
            logging.error(f"Failed to get_medical_specialities DepartmentService : {e}")
            raise e


    async def add_medical_specialities(self, medical_specialities : List[str]):
        try:
            await self.database.execute(CREATE_MEDICAL_SPECIALITIES_SCHEMA)
            for speciality in medical_specialities:
                await self.database.execute(INSERT_MEDICAL_SPECIALITIES_SCHEMA, speciality)
        except Exception as e:
            logging.error(f"Failed to add_medical_specialities DepartmentService : {e}")
            raise e