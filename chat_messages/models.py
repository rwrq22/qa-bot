# Related to Django package
from django.db import models

# Third party packages
import environ, os, requests
from pathlib import Path

# Django applications
from common.models import CommonModel
from chat_rooms.models import ChatRoom

DEBUG = "RENDER" not in os.environ
env = environ.Env()
if DEBUG:
    BASE_DIR = Path(__file__).resolve().parent.parent
    environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
A_URL = env("A_URL")


def get_model_answer(question, n):
    try:
        data = {"question": question, "n": n}
        response = requests.post(A_URL, json=data)
        result = response.json()
        if result["answer"] == "-1":
            return "잘 모르겠습니다."
        else:
            return result["answer"]
    except:
        return "An error occurred (ValidationError) when calling the InvokeEndpoint operation."


class Message(CommonModel):
    question = models.TextField(max_length=300)
    response = models.TextField(
        default="",
    )
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.SET_NULL, null=True)

    """ 답변 생성 함수(BERT Fine_Tuned 버전) """

    def generate_response(self):
        response = get_model_answer(self.question, 3)
        return response

    def save(self, *args, **kwargs):
        if not self.pk:
            self.response = self.generate_response()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.question[:30]}: {self.created_at}"
