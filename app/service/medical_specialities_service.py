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

    async def set_doctor_specialities(self, doctor_id: str, specialities: List[int]):
        create_query = """
            CREATE TABLE IF NOT EXISTS doctor_specialities (
                doctor_id INT REFERENCES doctors(id) ON DELETE CASCADE,
                speciality_id INT REFERENCES medical_specialities(id) ON DELETE CASCADE,
                PRIMARY KEY (doctor_id, speciality_id)
            );
        """
        await self.database.execute(create_query)
        insert_query = """
            INSERT INTO doctor_specialities (doctor_id, speciality_id) 
            VALUES ($1, $2)
            ON CONFLICT (doctor_id, speciality_id) DO NOTHING;
        """

        for speciality_id in specialities:
            try:
                await self.database.execute(insert_query, doctor_id, speciality_id)
                logging.info(f"Speciality {speciality_id} added for doctor {doctor_id}.")
            except Exception as e:
                logging.error(f"Failed to insert speciality {speciality_id} for doctor {doctor_id}: {e}")
                raise e