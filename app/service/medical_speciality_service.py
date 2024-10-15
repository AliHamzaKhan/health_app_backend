import logging

from app import Database


class MedicalSpecialityService:

    def __init__(self, database: Database):
        self.database = database


    async def get_all_medical_specialities(self):
        search_query = "SELECT * FROM medical_specialities"
        try:
            data = await self.database.fetch(search_query)
            return data
        except Exception as e:
            logging.error(f"Failed to fetch medical_specialities: {e}")
            raise e

