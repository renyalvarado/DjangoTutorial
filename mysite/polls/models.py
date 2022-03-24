import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    list_display = ("id", "question_text", "pub_date")

    def was_published_recently(self) -> bool:
        return self.pub_date >= (timezone.now() - datetime.timedelta(days=1))

    def __repr__(self):
        fields_and_values = [
            f"{field}={repr(getattr(self, field))}"
            for field in self.list_display
        ]
        return f"{self.__class__.__name__}({', '.join(fields_and_values)})"

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def add_new_votes(self, new_votes=1):
        self.votes = models.F("votes") + new_votes

    def __str__(self):
        return self.choice_text
