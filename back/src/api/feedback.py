from fastapi import APIRouter
from src.dto.feedback import UserFeedbackRequest
from src.services.feedback import FeedbackService


feedback_service = FeedbackService()
router = APIRouter()


@router.post("/userFeedback")
async def user_feedback(data: UserFeedbackRequest) -> None:
    feedback_service.log_user_feedback(data)
