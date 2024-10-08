# Related to Django package
from django.db import models

# Third party packages
import json, environ, os
from pathlib import Path
import boto3

# Django applications
from common.models import CommonModel
from chat_rooms.models import ChatRoom

DEBUG = "RENDER" not in os.environ
env = environ.Env()
if DEBUG:
    BASE_DIR = Path(__file__).resolve().parent.parent
    environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = env("AWS_DEFAULT_REGION")
AWS_ENDPOINT_NAME = env("AWS_ENDPOINT_NAME")


def get_model_answer(question, n):
    try:
        client = boto3.client(
            "sagemaker-runtime",
            region_name="ap-northeast-2",
        )
        response = client.invoke_endpoint(
            EndpointName=AWS_ENDPOINT_NAME,
            ContentType="application/json",
            Accept="application/json",
            Body=(json.dumps({"question": question, "n": n})),
        )
        result = json.loads(response["Body"].read())
        if result["answer"] == "-1":
            return "잘 모르겠습니다."
        else:
            return result["answer"]
    except:
        return "An error occurred (ValidationError) when calling the InvokeEndpoint operation."


class Message(CommonModel):
    question = models.TextField()
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
        return "Messages"
