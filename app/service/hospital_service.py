import logging
import uuid

from app import Database
from app.models.hospital import Hospital, HospitalRequest
from app.schema.app_schemas import CREATE_HOSPITAL_SCHEME, INSERT_HOSPITAL_SCHEMA, FIND_HOSPITAL_IN_CITY_SCHEMA, \
    FIND_HOSPITAL_VALUES_SCHEMA
from app.service.profile_service import ProfileService


class HospitalService:

    def __init__(self, database: Database):
        self.database = database

    async def get_hospitals(self, user_id: str):
        """
        Retrieve hospitals near the user based on the city in the user's profile.
        """

        profile = ProfileService(self.database)
        user_profile = await profile.get_user_profile(user_id)
        if not user_profile:
            logging.error(f"User profile not found for user_id: {user_id}")
            return []

        city = user_profile.get("city")
        if not city:
            logging.warning(f"No city found in user profile for user_id: {user_id}")
            return []

        # query = """
        #        SELECT * FROM hospitals WHERE city = $1
        #        """
        try:
            # Fetch hospitals in the same city
            hospitals_data = await self.database.fetch(FIND_HOSPITAL_IN_CITY_SCHEMA, city)
            if not hospitals_data:
                logging.info(f"No hospitals found in city: {city}")
                return []

            hospitals = []
            for row in hospitals_data:
                hospital = Hospital(
                    id=row["id"],
                    name=row["name"],
                    address=row["address"],
                    phone_number=row["phone_number"],
                    email=row["email"],
                    website=row.get("website"),
                    type=row.get("type"),
                    departments=row.get("departments"),
                    latlng=row.get("latlng"),
                    img=row.get("img"),
                    staff_count=row.get("staff_count"),
                )
                hospitals.append(hospital)

            return hospitals

        except Exception as e:
            logging.error(f"An error occurred while fetching hospitals for user_id {user_id} in city {city}: {e}")
            raise e

    async def add_hospital(self, hospital: HospitalRequest):
        """
        Add a new hospital or update an existing hospital by email (upsert operation).
        """
        # Create table if it doesn't exist
       #  create_table_query = """
       # CREATE TABLE IF NOT EXISTS hospitals (
       #     id VARCHAR(250) PRIMARY KEY,
       #     name VARCHAR(100),
       #     address TEXT,
       #     phone_number VARCHAR(15),
       #     email VARCHAR(100) UNIQUE,
       #     website VARCHAR(100),
       #     type VARCHAR(50),
       #     departments TEXT[],  -- Array of strings
       #     latlng VARCHAR(50),
       #     img TEXT,
       #     staff_count INT
       # );
       # """
        await self.database.execute(CREATE_HOSPITAL_SCHEME)

       #  insert_query = """
       # INSERT INTO hospitals (id, name, address, phone_number, email, website, type, departments, latlng, img, staff_count)
       # VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
       # ON CONFLICT (email) DO UPDATE SET
       #     id = EXCLUDED.id,
       #     name = EXCLUDED.name,
       #     address = EXCLUDED.address,
       #     phone_number = EXCLUDED.phone_number,
       #     website = EXCLUDED.website,
       #     type = EXCLUDED.type,
       #     departments = EXCLUDED.departments,
       #     latlng = EXCLUDED.latlng,
       #     img = EXCLUDED.img,
       #     staff_count = EXCLUDED.staff_count;
       # """
        try:
            hospital_id = str(uuid.uuid4())
            data_to_insert = (
                hospital_id,
                hospital.name,
                hospital.address,
                hospital.phone_number,
                hospital.email,
                hospital.website,
                hospital.type,
                hospital.departments,
                hospital.latlng,
                hospital.img,
                hospital.staff_count,
            )

            await self.database.execute(INSERT_HOSPITAL_SCHEMA, *data_to_insert)
            logging.info(f"Hospital '{hospital.name}' successfully added or updated.")
        except Exception as e:
            logging.error(f"Failed to add/update hospital '{hospital.name}': {e}")
            raise e

    async def get_hospital_values(self):
        # search_query = "SELECT id, name, latlng FROM hospitals;"
        try:
            data = await self.database.fetch(FIND_HOSPITAL_VALUES_SCHEMA)
            print(data)
            return [data]

        except Exception as e:
            logging.error(f"An error occurred while fetching hospitals ")
            raise e
