import logging

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from rest_framework import viewsets

from polls.services import Choice, Question, QuestionService
from polls.serializers import QuestionSerializer

logger = logging.getLogger(__name__)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = QuestionService.get_current_questions_and_their_votes()
    serializer_class = QuestionSerializer


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return QuestionService.get_current_questions_and_their_votes()[:5]


class DetailView(generic.DetailView):
    template_name = "polls/detail.html"
    context_object_name = "question"

    def get_queryset(self):
        return QuestionService.get_current_questions()


class ResultsViews(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    logger.info(f"Voting for question_id: {question_id}")
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice = request.POST["choice"]
        selected_choice = question.choice_set.get(pk=choice)
        logger.info(f"Selected choice: {choice}")
        selected_choice.add_new_votes()
        selected_choice.save()
        return HttpResponseRedirect(
            reverse("polls:results", args=(question.id,))
        )
    except (KeyError, Choice.DoesNotExist):
        logger.error(f"Choice does not exist: {choice}")
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "You didn't select a choice.",
        })
