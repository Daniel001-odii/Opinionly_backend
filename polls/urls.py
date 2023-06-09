from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    #path("<slug:slug>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    #path("<int:question_id>/vote/", views.vote, name="vote"),
    path("post/question/", views.questionPost, name="questionPost"),
    #path("questions/<int:question_id>/", views.poll_detail, name="detail"),
    path("questions/<slug:slug>/", views.poll_detail, name="detail"),
]