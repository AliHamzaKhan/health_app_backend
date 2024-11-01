import logging
import uuid
from typing import Optional, List
from app import Database
from app.models.doctor import DoctorRequest, Doctor
from app.schema.app_schemas import CREATE_DOCTOR_SCHEMA, INSERT_DOCTOR_SCHEME, FIND_DOCTOR_SPECIALITY_SCHEMA, \
    FIND_ALL_DOCTOR_SCHEMA, FIND_DOCTOR_BY_ID_SCHEMA, FIND_DOCTOR_IN_HOSPITAL_SCHEMA


class DoctorService:

    def __init__(self, database: Database):
        self.database = database

    async def add_doctor(self, request: DoctorRequest):
        doctor_id = str(uuid.uuid4())
        values = (
            doctor_id,
            request.name,
            request.email,
            request.degree,
            request.age,
            request.phone_no,
            request.gender,
            request.address, # Comma-separated string
            request.experience,
            request.image,
            request.availability,
        )
        try:
            await self.database.execute(CREATE_DOCTOR_SCHEMA)
            await self.database.execute(INSERT_DOCTOR_SCHEME, *values)
            await self.add_doctor_in_hospital(doctor_id, request.hospitals)
            await self.add_doctor_specializations(doctor_id, request.specialization)
            logging.info(f"Doctor {doctor_id} added successfully.")
        except Exception as e:
            logging.error(f"Failed to add doctor: {e}")
            raise e

        return {"id": doctor_id}

    async def get_doctor(self, doctor_id: str) -> Optional[Doctor]:
        # query =
        # "SELECT * FROM doctors WHERE id = $1"
        search_query = """
        SELECT doctors.*, 
            COALESCE(ARRAY_AGG(DISTINCT doctor_in_hospitals.hospital_id), ARRAY[]::VARCHAR[]) AS hospitals, 
            COALESCE(ARRAY_AGG(DISTINCT doctor_specializations.specialization_id), ARRAY[]::INT[]) AS specializations
            FROM doctors
            LEFT JOIN doctor_in_hospitals ON doctors.id = doctor_in_hospitals.doctor_id
            LEFT JOIN doctor_specializations ON doctors.id = doctor_specializations.doctor_id
            WHERE doctors.id = $1
            GROUP BY doctors.id;
        """
        try:
            # row = await self.database.fetchrow(FIND_DOCTOR_BY_ID_SCHEMA, doctor_id)  # Fetch single row using the doctor ID
            row = await self.database.fetchrow(search_query, doctor_id)
            if row:
                return row
            else:
                return None
        except Exception as e:
            logging.error(f"Failed to fetch doctor: {e}")
            raise e

    async def get_doctors_in_hospital(self, hospital_id: str):
        # query =
        # """
        #     SELECT * FROM doctors
        #     WHERE $1 = ANY(string_to_array(hospitals, ','))
        #     """
        search_query = """
        SELECT doctors.*, 
        COALESCE(ARRAY_AGG(DISTINCT doctor_in_hospitals.hospital_id), ARRAY[]::VARCHAR[]) AS hospitals,
        COALESCE(ARRAY_AGG(DISTINCT doctor_specializations.specialization_id), ARRAY[]::INT[]) AS specializations
        FROM doctors
        LEFT JOIN doctor_in_hospitals ON doctors.id = doctor_in_hospitals.doctor_id
        LEFT JOIN doctor_specializations ON doctors.id = doctor_specializations.doctor_id
        WHERE doctor_in_hospitals.hospital_id = $1
        GROUP BY doctors.id;
        """

        try:

            rows = await self.database.fetch(search_query, hospital_id)
            if not rows:
                return []
            else:
                return rows

        except Exception as e:
            logging.error(f"Failed to fetch doctors for hospital {hospital_id}: {e}")
            raise e

    async def find_doctors(self, speciality: Optional[str] = None):
        if not speciality:
            search_query = FIND_ALL_DOCTOR_SCHEMA
            # """
            #             SELECT * FROM doctors
            #         """
            params = ()

        else:
            search_query = FIND_DOCTOR_SPECIALITY_SCHEMA
            # """
            #        SELECT * FROM doctors
            #        WHERE EXISTS (
            #            SELECT 1 FROM unnest(string_to_array(specialization, ',')) AS specialization_item
            #            WHERE TRIM(specialization_item) ILIKE TRIM($1)
            #        )
            #    """
            params = (speciality,)
        try:
            rows = await self.database.fetch(search_query, *params)
            return rows

        except Exception as e:
            logging.error(f"Failed to fetch doctors for speciality {speciality}: {e}")
            raise e

    async def add_doctor_specializations(self, doctor_id: str, specialities: List[int]):
        create_query = """
            CREATE TABLE IF NOT EXISTS doctor_specializations (
                doctor_id VARCHAR REFERENCES doctors(id) ON DELETE CASCADE ON UPDATE CASCADE,
                specialization_id INT REFERENCES medical_specialities(id) ON DELETE CASCADE,
                PRIMARY KEY (doctor_id, specialization_id)
            );
        """
        try:
            await self.database.execute(create_query)
            insert_query = """
                INSERT INTO doctor_specializations (doctor_id, specialization_id) 
                VALUES ($1, $2)
                ON CONFLICT (doctor_id, specialization_id) DO NOTHING;
            """

            for specialization_id in specialities:
                try:
                    await self.database.execute(insert_query, doctor_id, specialization_id)
                    logging.info(f"Speciality {specialization_id} added for doctor {doctor_id}.")
                except Exception as e:
                    logging.error(f"Failed to insert speciality {specialization_id} for doctor {doctor_id}: {e}")
                    raise e
        except Exception as e:
            logging.error(f"Failed to create doctor_specializations table: {e}")

    async def add_doctor_in_hospital(self, doctor_id: str, hospital_id: List[str]):
        create_query = """
        CREATE TABLE IF NOT EXISTS doctor_in_hospitals (
                doctor_id VARCHAR REFERENCES doctors(id) ON DELETE CASCADE ON UPDATE CASCADE,
                hospital_id VARCHAR REFERENCES hospitals(id) ON DELETE CASCADE,
                PRIMARY KEY (doctor_id, hospital_id)
            );
        """
        try:
            await self.database.execute(create_query)
            insert_query = """
                INSERT INTO doctor_in_hospitals (doctor_id, hospital_id) 
                VALUES ($1, $2)
                ON CONFLICT (doctor_id, hospital_id) DO NOTHING;
            """

            for hospital in hospital_id:
                try:
                    await self.database.execute(insert_query, doctor_id, hospital)
                    logging.info(f"Hospital {hospital} added for doctor {doctor_id}.")
                except Exception as e:
                    logging.error(f"Failed to insert hospital {hospital} for doctor {doctor_id}: {e}")
                    raise e
        except Exception as e:
            logging.error(f"Failed to create doctor_hospitals table: {e}")


