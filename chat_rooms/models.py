from django.db import models

from common.models import CommonModel


class ChatRoom(CommonModel):
    session_key = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return f"ChatRoom {self.session_key}"
