from django.db import models
from common.models import CommonModel
from chat_rooms.models import ChatRoom
import json
import numpy as np
from pathlib import Path

# GPT-3.5 api
""" import openai

openai.api_key = env("OPENAI_API_KEY") """

# base-model, tokenizer, classifier-model
""" import torch
from transformers import BertForSequenceClassification, BertModel
from kobert_tokenizer import KoBERTTokenizer

device = torch.device("cpu")
MODEL_NAME = "bert_lib_v2"
classifier_model = BertForSequenceClassification.from_pretrained(MODEL_NAME)
classifier_model.to(device)
tokenizer = KoBERTTokenizer.from_pretrained("skt/kobert-base-v1")
base_model = BertModel.from_pretrained("skt/kobert-base-v1")

# Question vectors
with open("bert_lib_v2/qa_vectors_v3.json", "r", encoding="utf-8") as f:
    qa_vectors = {int(k): np.array(v) for k, v in json.load(f).items()}


# Get CLS Token Torch
def get_cls_token(sent_A):
    base_model.eval()
    tokenized_sent = tokenizer(
        sent_A,
        return_tensors="pt",
        truncation=True,
        add_special_tokens=True,
        max_length=32,
    ).to(device)
    with torch.no_grad():  # gradient 계산 비활성화
        outputs = base_model(
            input_ids=tokenized_sent["input_ids"],
            attention_mask=tokenized_sent["attention_mask"],
            token_type_ids=tokenized_sent["token_type_ids"],
        )
    logits = outputs.last_hidden_state[:, 0, :].detach().cpu().numpy()
    return logits


# Cosine similarity function
def custom_cosine_similarity(a, b):
    numerator = np.dot(a, b.T)
    a_norm = np.sqrt(np.sum(a * a))
    b_norm = np.sqrt(np.sum(b * b, axis=-1))

    denominator = a_norm * b_norm
    return numerator / denominator


# Get top n idx
def return_top_n_idx(question, n):
    question_vector = get_cls_token(question)
    sentence_similarity = {}
    for i in qa_vectors.keys():
        ir_vector = qa_vectors[i]
        similarity = custom_cosine_similarity(question_vector, ir_vector)
        sentence_similarity[i] = similarity

    sorted_sim = sorted(sentence_similarity.items(), key=lambda x: x[1], reverse=True)
    return sorted_sim[0:n]


# predict 함수
# 0: "non_similar", 1: "similar"
def sentences_predict(sent_A, sent_B):
    classifier_model.eval()
    tokenized_sent = tokenizer(
        sent_A,
        sent_B,
        return_tensors="pt",
        truncation=True,
        add_special_tokens=True,
        max_length=64,
    )

    with torch.no_grad():  # gradient 계산 비활성화
        outputs = classifier_model(
            input_ids=tokenized_sent["input_ids"],
            attention_mask=tokenized_sent["attention_mask"],
            token_type_ids=tokenized_sent["token_type_ids"],
        )

    logits = outputs[0]
    logits = logits.detach().cpu().numpy()
    result = np.argmax(logits)

    return result


import pandas as pd

data = pd.read_csv("bert_lib_v2/ChatbotData_v2.csv")
chatbot_Question = data["Q"].values
chatbot_Answer = data["A"].values


# 답변 생성 함수
def get_answer(question, n):
    results = return_top_n_idx(question, n)
    for result in results:
        ir_answer = chatbot_Answer[result[0]]
        ir_question = chatbot_Question[result[0]]
        if sentences_predict(question, ir_question) == 1:
            return ir_answer  # 정답 반환
    return "-1"  # "잘 모름"
    # return chatbot_Answer[results[0][0]]  # "몰라도 반환"
 """


class Message(CommonModel):
    question = models.TextField()
    response = models.TextField(
        default="",
    )
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.SET_NULL, null=True)

    ########### 답변 생성 함수(BERT Fine_Tuned 버전) ############
    def generate_response(self):
        response = "테스트"
        """response = get_answer(self.question, 3)"""
        """ response = self.generate_random_response() """
        """ if response == "-1":
            return "잘 모르겠습니다."
        else:
            return response """
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
