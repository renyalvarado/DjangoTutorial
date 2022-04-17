from django.db.models.aggregates import Sum
from polls.models import Question, Choice


class QuestionService:
    @staticmethod
    def get_current_questions():
        return Question.current_ones

    @classmethod
    def get_current_questions_and_their_votes(cls):
        return cls.get_current_questions() \
            .annotate(votes_sum=Sum("choice__votes"))
