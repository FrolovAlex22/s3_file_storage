from fastapi.responses import ORJSONResponse
import uvicorn
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBearer

from db.db import create_model
from api.router.s3_router import router_s3
from core.config import settings, s3_client
from api.router.auth_router import router_auth
from api.router.files_router import router_files


http_bearer = HTTPBearer(auto_error=False)

app = FastAPI(
    title=settings.app_title,
    default_response_class=ORJSONResponse,)
# app = FastAPI(
#     title=config.settings.app_title,
#     dependencies=[Depends(http_bearer)],
#     root_path="/sending_messages",
#     openapi_url="/openapi.json",
#     docs_url="/docs",
#     redoc_url="/redoc",
#     version="2.5.0",
# )

app.include_router(router_auth)
app.include_router(router_files, prefix="/files")

@app.on_event("startup")
async def startup_event():
    await create_model()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
# if __name__ == "__main__":
#     uvicorn.run(
#         "main:app",
#         host=config.settings.project_host,
#         port=config.settings.project_port,
#         reload=True,
#     )


# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbGV4IiwiZXhwIjoxNzI0NjkxMjY1fQ.I9pKv53UUQhaG8DPsKMaRL8l61p0p-XHv1Zf91PNkQc",
#   "token_type": "bearer"
# }