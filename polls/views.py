from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question
from django.contrib import messages
from django.db.models import Max
from django.db.models import F
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm #add this
from django.db.models import Prefetch

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator





#trying forms.....
from .forms import QuestionForm, ChoiceForm
# Create your views here.


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        queryset = Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")
        for question in queryset:
            highest_voted_choice = question.choice_set.aggregate(Max('votes'))
            highest_votes = highest_voted_choice['votes__max']
            highest_voted_choices = question.choice_set.filter(votes=highest_votes)
            question.highest_voted_choices = highest_voted_choices

        return queryset

        #return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]



def poll_list(request):
    latest_question_list = Question.objects.annotate(max_votes=Max('choice__votes')).filter(choice__votes=F('max_votes'))
    
    return render(request, 'polls/index.html', {'latest_question_list': latest_question_list})
    
    
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    
        


@login_required
def poll_detail(request, slug):
    question = get_object_or_404(Question, slug=slug)
    choice_form = None
    has_existing_choice = Choice.objects.filter(question=question, user=request.user).exists()

    if not has_existing_choice:
        if request.method == 'POST':
            choice_form = ChoiceForm(request.POST)
            if choice_form.is_valid():
                choice = choice_form.save(commit=False)
                choice.question = question
                choice.user = request.user
                choice.save()
                messages.success(request, "Choice added successfully.")
                return redirect('polls:detail', slug=question.slug)
        else:
            choice_form = ChoiceForm()

    existing_choice = Choice.objects.filter(question=question, user=request.user).first()

    if request.method == 'POST' and 'upvote' in request.POST:
        if existing_choice:
            existing_upvote = existing_choice.upvotes.filter(id=request.user.id).exists()
            if existing_upvote:
                messages.error(request, "You have already upvoted this choice.")
            else:
                existing_choice.upvotes.add(request.user)
                existing_choice.votes += 1
                existing_choice.save()
                messages.success(request, "Upvote recorded successfully.")

    if request.method == 'POST' and 'downvote' in request.POST:
        if existing_choice:
            existing_downvote = existing_choice.downvotes.filter(id=request.user.id).exists()
            if existing_downvote:
                messages.error(request, "You have already downvoted this choice.")
            else:
                existing_choice.downvotes.add(request.user)
                existing_choice.votes -= 1
                existing_choice.save()
                messages.success(request, "Downvote recorded successfully.")

    question.views += 1
    question.save()

    return render(request, 'polls/detail.html', {
        'question': question,
        'choice_form': choice_form,
    })







class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


"""
@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
"""       
        
@login_required
def questionPost(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, user=request.user)
        choice_forms = [ChoiceForm(request.POST, prefix=f'choice_form_{i}') for i in range(3)]

        if question_form.is_valid() and all([form.is_valid() for form in choice_forms]):
            question = question_form.save()
            for form in choice_forms:
                choice = form.save(commit=False)
                choice.question = question
                choice.save()
            messages.success(request, "Question and choices added successfully.")
            return HttpResponseRedirect(reverse("polls:index"))
        else:
            messages.error(request, "Failed to add question and choices. Please check the form data.")
    else:
        question_form = QuestionForm(user=request.user)
        choice_forms = [ChoiceForm(prefix=f'choice_form_{i}') for i in range(3)]

    return render(request, 'polls/post.html', {
        'question_form': question_form,
        'choice_forms': choice_forms,
    })
