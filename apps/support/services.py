"""Groq LLM client wrapper."""
from __future__ import annotations

import logging

from django.conf import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "Ти ввічливий асистент підтримки маркетплейсу handmade-товарів. "
    "Відповідай українською. Допомагай користувачам із питаннями про:\n"
    "• пошук та вибір товарів (прикраси, кераміка, одяг, іграшки, аксесуари, декор);\n"
    "• оформлення замовлення та оплату (на сайті — імітація оплати в один клік);\n"
    "• доставку та повернення;\n"
    "• роботу профілю майстра, публікацію власних виробів;\n"
    "• залишення відгуків (доступно після оплати).\n"
    "Якщо питання поза скоупом маркетплейсу — ввічливо переадресовуй до релевантних ресурсів. "
    "Тримай відповіді короткими (2–5 речень)."
)


def generate_reply(messages: list[dict[str, str]]) -> str:
    """Викликає Groq API та повертає текст відповіді.

    `messages` — список dict {"role": "user"|"assistant", "content": str}.
    """
    api_key = settings.GROQ_API_KEY
    if not api_key:
        logger.warning("GROQ_API_KEY не налаштовано; повертаю stub-відповідь.")
        return (
            "Підтримка тимчасово недоступна (не налаштовано ключ API). "
            "Спробуйте пізніше або напишіть на support@example.com."
        )

    from groq import Groq

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        max_tokens=512,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, *messages],
    )
    return (response.choices[0].message.content or "").strip() or "Вибачте, не вдалося сформувати відповідь."
