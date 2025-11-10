from fastapi import FastAPI
import src.config as config
from src.auth import router as auth_router

app = FastAPI(
    title=config.APP_NAME,
    swagger_ui_parameters={"persistAuthorization": True}
)


app.include_router(auth_router)





@app.get("/config-check")
async def config_check():
    return {
        'app': config.APP_NAME,
        'db_url': config.DATABASE_URL,
        'jwt': config.JWT_SECRET
    }