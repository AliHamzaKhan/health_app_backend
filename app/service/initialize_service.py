from app import Database
from app.service.auth_service import AuthService
from app.service.data_process_service import DataProcessService
from app.service.doctor_service import DoctorService
from app.service.hospital_service import HospitalService
from app.service.profile_service import ProfileService
from app.service.token_service import TokenService


database_url = "postgresql://aliawan:WizTech123a@localhost:5432/postgres"
db = Database(database_url)
auth_service = AuthService(db)
data_process_service = DataProcessService(db)
doctor_service = DoctorService(db)
hospital_service = HospitalService(db)
profile_service = ProfileService(db)
token_service = TokenService(db)