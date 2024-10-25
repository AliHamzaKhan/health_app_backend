from app import Database
from app.service.auth_service import AuthService
from app.service.data_process_service import DataProcessService
from app.service.department_service import DepartmentService
from app.service.doctor_service import DoctorService
from app.service.hospital_service import HospitalService
from app.service.medical_specialities_service import MedicalSpecialitiesService
from app.service.profile_service import ProfileService
from app.service.rating_service import RatingService
from app.service.token_service import TokenService
import os
from dotenv import load_dotenv
load_dotenv()


database_url = os.environ.get('DATABASE_URL')
# print('database_url', database_url)

db = Database(database_url)
auth_service = AuthService(db)
data_process_service = DataProcessService(db)
doctor_service = DoctorService(db)
hospital_service = HospitalService(db)
profile_service = ProfileService(db)
token_service = TokenService(db)
rating_service = RatingService(db)
departments_service = DepartmentService(db)
medical_speciality_service = MedicalSpecialitiesService(db)