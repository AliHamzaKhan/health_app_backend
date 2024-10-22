import logging
from app import Database
from app.schema.app_schemas import CREATE_DEPARTMENTS_SCHEMA, INSERT_DEPARTMENTS_SCHEMA, FIND_DEPARTMENTS_SCHEMA


class DepartmentService:

    def __init__(self, database : Database):
        self.database = database


    async def add_department(self, name : str):
        try:
            await self.database.execute(CREATE_DEPARTMENTS_SCHEMA)
            await self.database.execute(INSERT_DEPARTMENTS_SCHEMA, name)
            logging.info(f"DepartmentService '{name}' successfully added or updated.")

        except Exception as e:
            logging.error(f"Failed to add/update DepartmentService '{name}': {e}")
            raise e

    async def get_departments(self):
        try:
            data = await self.database.fetch(FIND_DEPARTMENTS_SCHEMA)
            if not data:
                return []
            else:
                return data

        except Exception as e:
            logging.error(f"Failed to get_departments DepartmentService : {e}")
            raise e