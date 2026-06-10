from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.models.sql_models import User
from app.core.rabbitmq import rabbitmq_client
from app.models.pydantic_schemas import VideoUploadRequest

router = APIRouter()

@router.post("/upload-video")
async def upload_video(
    request: VideoUploadRequest,
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can upload videos")
    
    # Вызов инфраструктурного сервиса напрямую из API слоя (или можно вынести в VideoService)
    await rabbitmq_client.send_video_conversion_task(request.video_path, request.course_id)
    return {"message": "Video uploaded and queued for conversion"}
