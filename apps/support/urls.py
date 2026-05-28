from django.urls import path

from . import views

app_name = "support"

urlpatterns = [
    path("", views.chat, name="chat"),
    path("new/", views.new_session, name="new_session"),
    path("<int:session_id>/send/", views.send_message, name="send"),
    path("<int:session_id>/poll/", views.poll, name="poll"),
]
