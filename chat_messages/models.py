from django.db import models
from common.models import CommonModel
from chat_rooms.models import ChatRoom
import json, environ, os
from pathlib import Path

env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = env("AWS_DEFAULT_REGION")
AWS_ENDPOINT_NAME = env("AWS_ENDPOINT_NAME")


# return chatbot_Answer[results[0][0]]  # "몰라도 반환"
def get_model_answer(question, n):
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


import boto3


class Message(CommonModel):
    question = models.TextField()
    response = models.TextField(
        default="",
    )
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.SET_NULL, null=True)

    ########### 답변 생성 함수(BERT Fine_Tuned 버전) ############
    def generate_response(self):
        response = get_model_answer(self.question, 3)
        return response

    def save(self, *args, **kwargs):
        if not self.pk:
            self.response = self.generate_response()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return "Messages"

    ########### 답변 생성 함수(openai 버전, 사용 불가) ############
    """ def generate_random_response(self):
        print("run!")
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a University library chatbot. Please provide concise and formal responses, like a librarian .You should respond that you don't know any information you can't figure out.",
                },
                {
                    "role": "user",
                    "content": f"{self.question}",
                },
            ],
        )
        return completion["choices"][0]["message"]["content"] """
