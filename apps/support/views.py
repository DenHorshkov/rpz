from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django_ratelimit.decorators import ratelimit

from .models import ChatMessage, ChatSession
from .tasks import generate_reply_task


@login_required
def chat(request):
    session = (
        ChatSession.objects.filter(user=request.user).order_by("-updated_at").first()
        or ChatSession.objects.create(user=request.user)
    )
    return render(
        request,
        "support/chat.html",
        {"session": session, "messages": session.messages.all()},
    )


@login_required
@require_POST
@ratelimit(key="user", rate="30/h", block=True)
def send_message(request, session_id: int):
    session = get_object_or_404(ChatSession, pk=session_id, user=request.user)
    text = (request.POST.get("text") or "").strip()
    if not text:
        return redirect("support:chat")
    ChatMessage.objects.create(session=session, role=ChatMessage.Role.USER, content=text)
    ChatMessage.objects.create(
        session=session, role=ChatMessage.Role.ASSISTANT, content="…", is_pending=True
    )
    session.save(update_fields=["updated_at"])
    generate_reply_task.delay(session.pk)
    return redirect("support:chat")


@login_required
def poll(request, session_id: int):
    session = get_object_or_404(ChatSession, pk=session_id, user=request.user)
    after = int(request.GET.get("after", 0))
    qs = session.messages.filter(pk__gt=after).order_by("created_at")
    data = [
        {
            "id": m.pk,
            "role": m.role,
            "content": m.content,
            "is_pending": m.is_pending,
            "created_at": m.created_at.isoformat(),
        }
        for m in qs
    ]
    return JsonResponse({"messages": data})


@login_required
@require_POST
def new_session(request):
    session = ChatSession.objects.create(user=request.user)
    return redirect("support:chat")
