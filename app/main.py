import asyncio

from fastapi import FastAPI
from app.api.api_routes import router, db
from app.payload.login_model import LoginModel
import app.service.initialize_service as service

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})
app.include_router(router)



async def main():
   await login()

async def login():
    try:
        await db.connect()
        data = await service.auth_service.login(
            user_type_id=3,
            phone_no='+923213203764',
            email='',
            fcm_token='login_model.fcm_token',
        )
        print(type(data))
        print(data)
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


if __name__ == "__main__":
    asyncio.run(main())