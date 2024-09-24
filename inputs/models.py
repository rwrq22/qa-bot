from django.db import models
from common.models import CommonModel


class Input(CommonModel):
    text = models.TextField()

    def __str__(self) -> str:
        return "Inputs"
