from ..dto.request import UserFeedbackRequest
from ..log.logger import get_feedback_logger


class FeedbackService:
    def __init__(self) -> None:
        self.feedback_logger = get_feedback_logger()

    def log_user_feedback(self, data: UserFeedbackRequest) -> None:
        self.feedback_logger.info({"session Id": data.session_id, "song Id": data.song_id, "is like": data.is_like})
