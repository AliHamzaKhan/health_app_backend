import logging
import uuid

from app import Database
from app.models.hospital import Hospital, HospitalRequest
from app.models.rating import RatingRequest, Rating
from app.service.profile_service import ProfileService


class HospitalService:

    def __init__(self, database: Database):
        self.database = database

    async def get_hospitals(self, user_id: str):
        """
        Retrieve hospitals near the user based on the city in the user's profile.
        """
        # Fetch user profile to get location details

        profile = ProfileService(self.database)
        user_profile = await profile.get_user_profile(user_id)
        if not user_profile:
            logging.error(f"User profile not found for user_id: {user_id}")
            return []

        city = user_profile.get("city")
        if not city:
            logging.warning(f"No city found in user profile for user_id: {user_id}")
            return []

        query = """
               SELECT * FROM hospitals WHERE city = $1
               """
        try:
            # Fetch hospitals in the same city
            hospitals_data = await self.database.fetch(query, city)
            if not hospitals_data:
                logging.info(f"No hospitals found in city: {city}")
                return []

            hospitals = []
            for row in hospitals_data:
                ratings = await self.get_hospital_ratings(row["id"])  # Fetch ratings for each hospital
                hospital = Hospital(
                    id=row["id"],
                    name=row["name"],
                    address=row["address"],
                    phone_number=row["phone_number"],
                    email=row["email"],
                    website=row.get("website"),
                    type=row.get("type"),
                    departments=row.get("departments"),
                    rating=ratings,  # Set ratings here
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
        create_table_query = """
       CREATE TABLE IF NOT EXISTS hospitals (
           id VARCHAR(250) PRIMARY KEY,
           name VARCHAR(100),
           address TEXT,
           phone_number VARCHAR(15),
           email VARCHAR(100) UNIQUE,
           website VARCHAR(100),
           type VARCHAR(50),
           departments TEXT[],  -- Array of strings
           latlng VARCHAR(50),
           img TEXT,
           staff_count INT
       );
       """
        await self.database.execute(create_table_query)

        # Insert or update hospital based on email
        insert_query = """
       INSERT INTO hospitals (id, name, address, phone_number, email, website, type, departments, latlng, img, staff_count)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
       ON CONFLICT (email) DO UPDATE SET
           id = EXCLUDED.id,
           name = EXCLUDED.name,
           address = EXCLUDED.address,
           phone_number = EXCLUDED.phone_number,
           website = EXCLUDED.website,
           type = EXCLUDED.type,
           departments = EXCLUDED.departments,
           latlng = EXCLUDED.latlng,
           img = EXCLUDED.img,
           staff_count = EXCLUDED.staff_count;
       """
        try:
            data_to_insert = (
                hospital.id,
                hospital.name,
                hospital.address,
                hospital.phone_number,
                hospital.email,
                hospital.website,
                hospital.type,
                hospital.departments,  # Storing departments as an array
                hospital.latlng,
                hospital.img,
                hospital.staff_count,
            )

            await self.database.execute(insert_query, *data_to_insert)
            logging.info(f"Hospital '{hospital.name}' successfully added or updated.")
        except Exception as e:
            logging.error(f"Failed to add/update hospital '{hospital.name}': {e}")
            raise e

    async def add_hospital_rating(self, rating: RatingRequest):
        """
        Insert a new rating for a hospital into the hospitals_rating table.
        """
        # Create the ratings table if it doesn't exist
        create_table_query = """
           CREATE TABLE IF NOT EXISTS hospitals_rating (
               id VARCHAR(250) PRIMARY KEY,
               hospital_id VARCHAR(250) NOT NULL,
               user_id VARCHAR(250) NOT NULL,
               rating FLOAT CHECK (rating >= 0 AND rating <= 5),
               comment TEXT,
               FOREIGN KEY (hospital_id) REFERENCES hospitals(id) ON DELETE CASCADE,
               FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
           );
       """
        await self.database.execute(create_table_query)

        # Insert or update the rating if it exists (based on the rating ID)
        insert_query = """
           INSERT INTO hospitals_rating (id, hospital_id, user_id, rating, comment)
           VALUES ($1, $2, $3, $4, $5)
           ON CONFLICT (id) DO UPDATE SET
               rating = EXCLUDED.rating,
               comment = EXCLUDED.comment;
       """

        # Ensure that the rating ID is a valid UUID
        rating_id = str(uuid.uuid4())  # Automatically generate a unique rating ID if needed

        data_to_insert = (
            rating_id,
            rating.hospital_id,
            rating.user_id,
            rating.rating,
            rating.comment
        )

        try:
            await self.database.execute(insert_query, *data_to_insert)
            logging.info(f"Successfully added/updated rating for hospital ID: {rating.hospital_id}")
        except Exception as e:
            logging.error(f"An error occurred while adding hospital rating: {e}")
            raise e

    async def get_hospital_ratings(self, hospital_id: str):
        """
        Fetch all ratings for a specific hospital from the hospitals_rating table.
        """
        query = """
       SELECT * FROM hospitals_rating WHERE hospital_id = $1
       """
        try:
            ratings_data = await self.database.fetch(query, hospital_id)
            if not ratings_data:
                logging.info(f"No ratings found for hospital ID: {hospital_id}")
                return []

            return [Rating(**row) for row in ratings_data]
        except Exception as e:
            logging.error(f"An error occurred while fetching ratings for hospital ID {hospital_id}: {e}")
            raise e