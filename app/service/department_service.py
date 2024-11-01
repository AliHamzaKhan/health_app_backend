import logging
from typing import List

from app import Database
from app.schema.app_schemas import CREATE_DEPARTMENTS_SCHEMA, INSERT_DEPARTMENTS_SCHEMA, FIND_DEPARTMENTS_SCHEMA


class DepartmentService:

    def __init__(self, database: Database):
        self.database = database

    async def add_department(self, name: str):
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

    async def initialize_table(self):
        # Create the table once
        create_query = """
        CREATE TABLE IF NOT EXISTS hospital_departments (
            hospital_id VARCHAR REFERENCES hospitals(id) ON DELETE CASCADE ON UPDATE CASCADE,
            department_id INT REFERENCES departments(department_id) ON DELETE CASCADE,
            PRIMARY KEY (hospital_id, department_id)
        );
        """
        await self.database.execute(create_query)

    async def set_hospital_department(self, department_ids: List[int], hospital_id: str):
        print('hospital_id1:', hospital_id)
        await self.initialize_table()
        insert_query = """
                INSERT INTO hospital_departments (hospital_id, department_id) 
                VALUES ($1, $2)
                ON CONFLICT (hospital_id, department_id) DO NOTHING;
                """

        try:
            for dept_id in department_ids:
                try:
                    await self.database.execute(insert_query, hospital_id, dept_id)
                    logging.info(f"Department {dept_id} added for hospital {hospital_id}.")
                except Exception as e:
                    logging.error(f"Failed to insert department {dept_id} for hospital {hospital_id}: {e}")
                    raise e

        except Exception as e:
            logging.error(f"Failed to set_hospital_department in DepartmentService: {e}")
            raise e
