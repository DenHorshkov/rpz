from django.conf import settings
from django.db import models


class ChatSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_sessions",
        verbose_name="Користувач",
    )
    created_at = models.DateTimeField("Створено", auto_now_add=True)
    updated_at = models.DateTimeField("Оновлено", auto_now=True)

    class Meta:
        verbose_name = "Сесія чату"
        verbose_name_plural = "Сесії чату"
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return f"Чат #{self.pk} ({self.user})"


class ChatMessage(models.Model):
    class Role(models.TextChoices):
        USER = "user", "Користувач"
        ASSISTANT = "assistant", "Асистент"

    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Сесія",
    )
    role = models.CharField("Роль", max_length=16, choices=Role.choices)
    content = models.TextField("Текст")
    is_pending = models.BooleanField("Очікує відповіді", default=False)
    created_at = models.DateTimeField("Створено", auto_now_add=True)

    class Meta:
        verbose_name = "Повідомлення"
        verbose_name_plural = "Повідомлення"
        ordering = ["created_at"]
