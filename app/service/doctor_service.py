import logging
import uuid
from typing import Optional
from app import Database
from app.models.doctor import DoctorRequest, Doctor


class DoctorService:

    def __init__(self, database: Database):
        self.database = database

    async def add_doctor(self, request: DoctorRequest):
        query = """
    INSERT INTO doctors (id, name, email, degree, age, phone_no, gender, address, hospitals, specialization, 
                         experience, image, availability, rating)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
    """
        doctor_id = str(uuid.uuid4())  # Generate a unique doctor ID

        # Prepare values for insertion
        values = (
            doctor_id,
            request.name,
            request.email,
            request.degree,
            request.age,
            request.phone_no,
            request.gender,
            request.address,
            ",".join(request.hospitals),  # Store hospitals as a comma-separated string
            request.specialization,
            request.experience,
            request.image,
            request.availability,
            request.rating
        )

        try:
            # Execute the insertion query
            await self.database.execute(query, *values)
            logging.info(f"Doctor {doctor_id} added successfully.")
        except Exception as e:
            logging.error(f"Failed to add doctor: {e}")
            raise e

        return {"id": doctor_id}

    async def get_doctor(self, doctor_id: str) -> Optional[Doctor]:
        query = "SELECT * FROM doctors WHERE id = $1"

        try:
            row = await self.database.fetchrow(query, doctor_id)  # Fetch single row using the doctor ID
            if row:
                # Convert hospitals from comma-separated string back to list
                hospitals_list = row["hospitals"].split(",") if row["hospitals"] else []

                # Create and return a Doctor model populated with the retrieved data
                return Doctor(
                    id=row["id"],
                    name=row["name"],
                    email=row["email"],
                    degree=row["degree"],
                    age=row["age"],
                    phone_no=row["phone_no"],
                    gender=row["gender"],
                    address=row["address"],
                    hospitals=hospitals_list,
                    specialization=row.get("specialization"),
                    experience=row.get("experience"),
                    image=row.get("image"),
                    availability=row.get("availability"),
                    rating=row.get("rating")
                )
            return None
        except Exception as e:
            logging.error(f"Failed to fetch doctor: {e}")
            raise e

    async def get_doctors_in_hospital(self, hospital_id: str):
        query = """
            SELECT * FROM doctors
            WHERE $1 = ANY(string_to_array(hospitals, ','))
            """

        try:
            # Fetch all doctors associated with the hospital_id
            rows = await self.database.fetch(query, hospital_id)

            # If no doctors are found, return an empty list
            if not rows:
                return []

            # Process each row and convert hospitals back to a list
            doctors = []
            for row in rows:
                hospitals_list = row["hospitals"].split(",") if row["hospitals"] else []

                # Create a Doctor object for each row
                doctors.append(Doctor(
                    id=row["id"],
                    name=row["name"],
                    email=row["email"],
                    degree=row["degree"],
                    age=row["age"],
                    phone_no=row["phone_no"],
                    gender=row["gender"],
                    address=row["address"],
                    hospitals=hospitals_list,
                    specialization=row.get("specialization"),
                    experience=row.get("experience"),
                    image=row.get("image"),
                    availability=row.get("availability"),
                    rating=row.get("rating")
                ))

            return doctors

        except Exception as e:
            logging.error(f"Failed to fetch doctors for hospital {hospital_id}: {e}")
            raise e
