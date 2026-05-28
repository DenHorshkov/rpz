from unittest.mock import patch

import pytest

from apps.support.models import ChatMessage, ChatSession
from apps.support.tasks import generate_reply_task


@pytest.mark.django_db
def test_generate_reply_task_creates_assistant_message(buyer):
    session = ChatSession.objects.create(user=buyer)
    ChatMessage.objects.create(session=session, role=ChatMessage.Role.USER, content="Привіт")
    ChatMessage.objects.create(
        session=session, role=ChatMessage.Role.ASSISTANT, content="…", is_pending=True
    )

    with patch("apps.support.tasks.generate_reply", return_value="Доброго дня! Чим допомогти?"):
        generate_reply_task.apply(args=[session.pk]).get()

    assistant_msgs = session.messages.filter(role=ChatMessage.Role.ASSISTANT, is_pending=False)
    assert assistant_msgs.count() == 1
    assert "Доброго дня" in assistant_msgs.first().content
    assert session.messages.filter(is_pending=True).count() == 0
