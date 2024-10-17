from datetime import datetime
from typing import Optional
from PIL import Image
from fastapi import APIRouter, UploadFile, File, FastAPI, Form, Body, Query
from app.ai.my_gemini import MyGemini
from app.constant.prompts import Prompts
from app.models.ai_request_enum import AiRequestType
from app.models.data_process import DataProcessRequest, DataProcess
from app.models.doctor import DoctorRequest
from app.models.hospital import HospitalRequest
from app.models.rating import RatingRequest, HospitalRatingRequest, DoctorRatingRequest
from app.models.token_used import TokenUsedRequest
from app.models.user_profile import UserProfileRequest
import app.service.initialize_service as service
from app.payload.login_model import LoginModel
from app.payload.used_token_request import UsedTokenRequestPayload
from app.utils.app_utils import convert_image_to_base64

app = FastAPI()
router = APIRouter()
app.include_router(router)
db = service.db


@router.get("/")
def read_root():
    return 'server is working'


@router.post("/login")
async def login(login_model: LoginModel):
    try:
        await db.connect()
        data = await service.auth_service.login(
            user_type_id=login_model.user_type_id,
            phone_number=login_model.phone_number,
            email=login_model.email,
            fcm_token=login_model.fcm_token,
        )
        print(type(data))
        if not data:
            return {
                'success': True,
                'data': {},
                'message': 'Successful'
            }

        return {
            'success': True,
            'data': {'login': data},
            'message': 'Successful'
        }

    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'success': False,
            'data': {},
            'message': 'error'
        }
    finally:
        await db.close()


@router.get("/get_user_types")
async def get_user_types():
    try:
        await db.connect()
        data = await service.auth_service.get_user_types()
        if not data:
            return {
                'success': True,
                'data': {'user_types': []},
                'message': 'Successful'
            }
        return {
            'success': True,
            'data': {'user_types': data},
            'message': 'Successful'
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'success': False,
            'data': {},
            'message': 'error'
        }
    finally:
        await db.close()


@router.get("/packages")
async def get_packages():
    try:
        await db.connect()
        data = await service.auth_service.get_packages()
        if not data:
            return {
                'success': True,
                'data': {'packages': []},
                'message': 'Successful'
            }

        return {
            'success': True,
            'data': {'packages': data},
            'message': 'Successful'
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'success': False,
            'data': {},
            'message': 'error'
        }
    finally:
        await db.close()


@router.get("/get_profile/{id}")
async def get_profile(id: str):
    try:
        await db.connect()
        retrieved_profile = await service.profile_service.get_user_profile(id)
        print("Retrieved Profile:", retrieved_profile)
        if not retrieved_profile:
            return {
                'success': True,
                'data': {},
                'message': 'Successful'
            }

        return {
            'success': True,
            'data': {'profile': retrieved_profile},
            'message': 'Successful'
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'success': False,
            'data': {},
            'message': 'error'
        }
    finally:
        await db.close()


@router.post("/save_profile")
async def save_profile(profile: UserProfileRequest):
    try:

        await db.connect()
        await service.profile_service.save_user_profile(profile)
        print("Profile added or updated successfully!")

        return {
            'success': True,
            'data': profile,
            'message': 'Successful'
        }
    except Exception as e:
        print(f"Error occurred while saving profile: {e}")
        return {
            'success': False,
            'data': {},
            'message': 'error'
        }
    finally:
        await db.close()


@router.post("/process_data")
async def process_data(
        userId: str = Body(...),
        ai_request_type: AiRequestType = Body(...),
        image: UploadFile = File(...)
):
    try:
        await db.connect()
        user = await service.auth_service.get_user_by_id(user_id=userId)

        if user is None:
            print('ai_tokens', 'not found')
            return {
                'success': False,
                'data': {},
                'message': 'error'
            }
        else:
            ai_tokens = user.get('ai_tokens')
            if ai_tokens < 100:
                return {
                    'success': False,
                    'data': {},
                    'message': 'insufficient ai_tokens'
                }
            else:
                print('ai_tokens', ai_tokens)

                open_img = Image.open(image.file)
                img = open_img.convert('RGB')

                gemini = MyGemini()
                ai_generated_response, token_used = gemini.generate_ai(ai_request_type, img)
                prompt = Prompts(ai_request_type)

                base_64_img = await  convert_image_to_base64(image)
                data_process = DataProcessRequest(
                    user_id=userId,
                    prompt=prompt.get_instructions(),
                    image_url=base_64_img,
                    ai_generated_text=ai_generated_response,
                    request_type=ai_request_type,
                    token_used=token_used
                )

                await db.connect()
                process_id = await service.data_process_service.save_data_process(data_process=data_process)
                await service.token_service.save_used_token(token_used, userId, process_id)
                await  service.token_service.update_user_ai_tokens(user_id=userId, token=token_used)
                payload_model = DataProcess(
                    id=process_id,
                    user_id=userId,
                    prompt=prompt.get_instructions(),
                    image_url=base_64_img,
                    ai_generated_text=ai_generated_response,
                    request_type=ai_request_type,
                    token_used=token_used,
                    created_at=datetime.utcnow()
                )
                return {
                    'success': True,
                    'data': {'data_process': payload_model},
                    'message': 'Successful'
                }

    except Exception as e:
        print(f"Error occurred while process_data: {e}")
        return {
            'success': False,
            'data': {},
            'message': 'error'
        }

    finally:
        await db.close()


@router.post("/get_process_data")
async def get_process_data(
        userId: str = Body(...),
        ai_request_type: Optional[AiRequestType] = Body(None)
):
    try:
        await  db.connect()
        process_data_list = await service.data_process_service.get_data_process(userId, ai_request_type)
        if not process_data_list:
            return {
                'success': True,
                'data': {},
                'message': 'Successful'
            }
        return {
            'success': True,
            'data': {'process_data': process_data_list},
            'message': 'Successful'
        }
    except Exception as e:
        print(f"Error occurred while saving profile: {e}")
        return {
            'success': False,
            'data': {},
            'message': 'error'
        }
    finally:
        await db.close()


@router.post("/get_hospitals")
async def get_nearby_hospital(user_id: str = Body(...)):
    try:
        await db.connect()
        data = service.hospital_service.get_hospitals(user_id)
        if not data:
            return {
                'success': True,
                'data': {},
                'message': 'Successful'
            }
        return {
            'success': True,
            'data': {'hospitals': data},
            'message': 'Successful'
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'success': False,
            'data': {},
            'message': 'error'
        }
    finally:
        await db.close()


@router.post("/add_hospital")
async def add_hospital(hospital: HospitalRequest):
    try:
        await db.connect()
        await service.hospital_service.add_hospital(hospital)
        return {
            'success': True,
            'data': {hospital},
            'message': 'Successful'
        }

    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'success': False,
            'data': {},
            'message': 'error'
        }
    finally:
        await db.close()


@router.get("/get_hospitals_value")
async def get_hospitals_value():
    try:
        await db.connect()
        data = await service.hospital_service.get_hospital_values()
        return {
            'success': True,
            'data': {'hospitals': data},
            'message': 'Successful'
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'success': False,
            'data': {},
            'message': 'error'
        }
    finally:
        await db.close()


@router.post("/add_doctor")
async def add_hospital(doctor: DoctorRequest):
    try:
        await db.connect()
        await service.doctor_service.add_doctor(doctor)
        return {
            'success': True,
            'data': {doctor},
            'message': 'Successful'
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'success': False,
            'data': {},
            'message': 'error'
        }
    finally:
        await db.close()


@router.get("/get_doctors/{doctor_id}")
async def get_doctor(doctor_id: str):
    try:
        await db.connect()
        doctor = await service.doctor_service.get_doctor(doctor_id)
        if not doctor:
            return {
                'success': True,
                'data': {},
                'message': 'No data found'
            }
        return {
            'success': True,
            'data': {'doctors': doctor},
            'message': 'Successful'
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'success': False,
            'data': {},
            'message': 'error'
        }
    finally:
        await db.close()


@router.get("/get_doctors_in_hospital/{hospital_id}")
async def get_doctors_in_hospital(hospital_id: str):
    try:
        await db.connect()
        doctors = await service.doctor_service.get_doctors_in_hospital(hospital_id)
        if not doctors:
            return {
                'success': True,
                'data': {},
                'message': 'Successful'
            }
        return {
            'success': True,
            'data': {'doctors': doctors},
            'message': 'Successful'
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'success': False,
            'data': {},
            'message': 'error'
        }

    finally:
        await db.close()


@router.post("/find_doctors")
async def find_doctors(speciality: str = Body(...), user_id: str = Body(...)):
    try:
        await db.connect()
        data = await service.doctor_service.find_doctors(speciality)
        if not data:
            return {
                'success': True,
                'data': {},
                'message': 'Successful'
            }
        return {
            'success': True,
            'data': {'doctors': data},
            'message': 'Successful'
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'success': False,
            'data': {},
            'message': 'error'
        }

    finally:
        await db.close()


@router.post("/add_used_token")
async def add_used_token(token: TokenUsedRequest):
    try:
        await db.connect()
        await service.token_service.save_used_token(token_used=token.token_used, user_id=token.user_id,
                                                    process_id=token.data_process_id)
        return {
            'success': True,
            'data': {'TokenUsedRequest': token},
            'message': 'Successful'
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'success': False,
            'data': {},
            'message': 'error'
        }
    finally:
        await db.close()


@router.post("/get_used_token")
async def get_used_token(token_request: UsedTokenRequestPayload):
    try:
        await db.connect()
        used_tokens = await service.token_service.get_used_token(token_request.user_id, token_request.data_process_id)
        if not used_tokens:
            return {
                'success': True,
                'data': {},
                'message': 'Successful'
            }
        return {
            'success': True,
            'data': {'tokens': used_tokens},
            'message': 'Successful'
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'success': False,
            'data': {},
            'message': 'error'
        }

    finally:
        await db.close()


@router.get("/get_all_medical_speciality")
async def get_all_medical_speciality():
    try:
        await db.connect()
        data = await service.medical_speciality_service.get_all_medical_specialities()
        if not data:
            return {
                'success': True,
                'data': {},
                'message': 'Successful'
            }
        return {
            'success': True,
            'data': {'medical': data},
            'message': 'Successful'
        }

    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'success': False,
            'data': {},
            'message': 'error'
        }

    finally:
        await db.close()


@router.post("/add_hospital_rating")
async def add_hospital_rating(hospital_rating: HospitalRatingRequest):
    try:
        await db.connect()
        await service.rating_service.add_hospital_rating(hospital_rating)
        return {
            'success': True,
            'data': {hospital_rating},
            'message': 'Successful'
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'success': False,
            'data': {},
            'message': 'error'
        }
    finally:
        await db.close()


@router.post("/get_hospital_rating")
async def get_hospital_rating(hospital_id: str = Body(...)):
    try:
        await db.connect()
        ratings = await service.rating_service.get_hospital_ratings(hospital_id)
        return {
            'success': True,
            'data': {'ratings': ratings},
            'message': 'Successful'
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'success': False,
            'data': {},
            'message': 'error'
        }
    finally:
        await db.close()


@router.post("/add_doctor_rating")
async def add_hospital_rating(doctor_rating: DoctorRatingRequest):
    try:
        await db.connect()
        await service.rating_service.add_doctor_rating(doctor_rating)
        return {
            'success': True,
            'data': {doctor_rating},
            'message': 'Successful'
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'success': False,
            'data': {},
            'message': 'error'
        }
    finally:
        await db.close()


@router.post("/get_doctor_rating")
async def get_hospital_rating(doctor_id: str = Body(...)):
    try:
        await db.connect()
        ratings = await service.rating_service.get_doctor_ratings(doctor_id)
        return {
            'success': True,
            'data': {'ratings': ratings},
            'message': 'Successful'
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'success': False,
            'data': {},
            'message': 'error'
        }
    finally:
        await db.close()
