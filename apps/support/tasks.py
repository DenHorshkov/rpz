import logging

from celery import shared_task

from .models import ChatMessage, ChatSession
from .services import generate_reply

logger = logging.getLogger(__name__)

HISTORY_LIMIT = 20


@shared_task(bind=True, max_retries=2, default_retry_delay=10)
def generate_reply_task(self, session_id: int) -> int:
    """Бере останні повідомлення сесії, кличе Claude, зберігає відповідь.

    Повертає id створеного ChatMessage(assistant).
    """
    session = ChatSession.objects.get(pk=session_id)
    history = list(
        session.messages.order_by("-created_at")[:HISTORY_LIMIT]
    )
    history.reverse()
    payload = [{"role": m.role, "content": m.content} for m in history if not m.is_pending]

    try:
        reply_text = generate_reply(payload)
    except Exception as exc:  # noqa: BLE001
        logger.exception("Anthropic call failed")
        try:
            self.retry(exc=exc)
        except self.MaxRetriesExceededError:
            reply_text = "Вибачте, асистент тимчасово недоступний. Спробуйте пізніше."

    msg = ChatMessage.objects.create(
        session=session,
        role=ChatMessage.Role.ASSISTANT,
        content=reply_text,
    )
    session.messages.filter(is_pending=True).delete()
    return msg.pk
