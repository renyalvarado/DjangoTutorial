from django.urls import include, path
from rest_framework import routers

from polls import views

router = routers.DefaultRouter()
router.register("rest-questions", views.QuestionViewSet)

app_name = "polls"

urlpatterns = [
    # /polls/
    path("", views.IndexView.as_view(), name="index"),

    # /polls/5/
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),

    # /polls/5/results
    path("<int:pk>/results/", views.ResultsViews.as_view(), name="results"),

    # /polls/5/vote
    path("<int:question_id>/vote/", views.vote, name="vote"),

    # /polls/api/
    path('api/', include(router.urls)),
]
