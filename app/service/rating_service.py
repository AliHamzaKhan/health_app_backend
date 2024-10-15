import logging
import uuid
from typing import List

from app import Database
from app.models.rating import RatingRequest, Rating, HospitalRatingRequest, HospitalRating, DoctorRatingRequest, \
    DoctorRating


class RatingService:

    def __init__(self, database: Database):
        self.database = database

    async def add_hospital_rating(self, rating: HospitalRatingRequest):
        """
        Insert or update a rating for a hospital into the hospitals_rating table.
        """
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

        insert_query = """
            INSERT INTO hospitals_rating (id, hospital_id, user_id, rating, comment)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (id) DO UPDATE SET
                rating = EXCLUDED.rating,
                comment = EXCLUDED.comment;
        """

        rating_id = str(uuid.uuid4())
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
            logging.error(f"Error while adding/updating hospital rating: {e}")
            raise

    async def get_hospital_ratings(self, hospital_id: str) -> List[HospitalRating]:
        """
        Fetch all ratings for a specific hospital from the hospitals_rating table.
        """
        query = """
            SELECT * FROM hospitals_rating WHERE hospital_id = $1;
        """

        try:
            ratings_data = await self.database.fetch(query, hospital_id)
            if not ratings_data:
                logging.info(f"No ratings found for hospital ID: {hospital_id}")
                return []

            return [HospitalRating(**row) for row in ratings_data]
        except Exception as e:
            logging.error(f"Error while fetching ratings for hospital ID {hospital_id}: {e}")
            raise

    async def add_doctor_rating(self, rating: DoctorRatingRequest):
        """
        Insert or update a rating for a doctor into the doctor_rating table.
        """
        create_table_query = """
            CREATE TABLE IF NOT EXISTS doctor_rating (
                id VARCHAR(250) PRIMARY KEY,
                doctor_id VARCHAR(250) NOT NULL,
                user_id VARCHAR(250) NOT NULL,
                rating FLOAT CHECK (rating >= 0 AND rating <= 5),
                comment TEXT,
                FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """
        await self.database.execute(create_table_query)

        insert_query = """
            INSERT INTO doctor_rating (id, doctor_id, user_id, rating, comment)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (id) DO UPDATE SET
                rating = EXCLUDED.rating,
                comment = EXCLUDED.comment;
        """

        rating_id = str(uuid.uuid4())
        data_to_insert = (
            rating_id,
            rating.doctor_id,
            rating.user_id,
            rating.rating,
            rating.comment
        )

        try:
            await self.database.execute(insert_query, *data_to_insert)
            logging.info(f"Successfully added/updated rating for doctor ID: {rating.doctor_id}")
        except Exception as e:
            logging.error(f"Error while adding/updating doctor rating: {e}")
            raise

    async def get_doctor_ratings(self, doctor_id: str) -> List[DoctorRating]:
        """
        Fetch all ratings for a specific doctor from the doctor_rating table.
        """
        query = """
            SELECT * FROM doctor_rating WHERE doctor_id = $1;
        """

        try:
            ratings_data = await self.database.fetch(query, doctor_id)
            if not ratings_data:
                logging.info(f"No ratings found for doctor ID: {doctor_id}")
                return []

            return [DoctorRating(**row) for row in ratings_data]
        except Exception as e:
            logging.error(f"Error while fetching ratings for doctor ID {doctor_id}: {e}")
            raise