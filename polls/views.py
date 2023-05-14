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
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm #add this


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
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

def poll_list(request):
    latest_question_list = Question.objects.annotate(max_votes=Max('choice__votes')).filter(choice__votes=F('max_votes'))
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    
    return render(request, 'polls/index.html', {'latest_question_list': latest_question_list})



def poll_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choice_form = ChoiceForm(request.POST or None)

    if request.method == 'POST':
        if choice_form.is_valid():
            # Check if the user has already submitted a choice
            existing_choice = Choice.objects.filter(
                question=question, user=request.user
            ).exists()
            if existing_choice:
                messages.error(request, "You have already submitted a choice.")
            else:
                choice = choice_form.save(commit=False)
                choice.question = question
                choice.user = request.user
                choice.save()
                messages.success(request, "Choice added successfully.")
                choice_form = ChoiceForm()  # Reset the form after saving the choice
        else:
            selected_choice_id = request.POST.get('choice')
            selected_choice = get_object_or_404(Choice, pk=selected_choice_id)
            
            # Check if the user has already upvoted the choice
            existing_upvote = selected_choice.upvotes.filter(id=request.user.id).exists()
            if existing_upvote:
                messages.error(request, "You have already upvoted this choice.")
            else:
                selected_choice.upvotes.add(request.user)
                selected_choice.votes += 1
                selected_choice.save()
                messages.success(request, "Upvote recorded successfully.")
    
    return render(request, 'polls/detail.html', {
        'question': question,
        'choice_form': choice_form,
    })







class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


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
        
        
        


def questionPost(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        choice_form = ChoiceForm(request.POST)
        
        if question_form.is_valid():
            question = question_form.save()
            
            if choice_form.is_valid():
                choice = choice_form.save(commit=False)
                choice.question = question
                choice.user = request.user
                choice.save()
                return HttpResponseRedirect(reverse("polls:index"))
                
            # Redirect or do something else
            
    else:
        question_form = QuestionForm()
        choice_form = ChoiceForm()
    
    return render(request, 'polls/post.html', {'question_form': question_form, 'choice_form': choice_form})




#from django.shortcuts import  render, redirect

#from django.contrib import messages

def register_request(request):
    if request.method == "POST":
      form = NewUserForm(request.POST)
      if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Registration successful." )
        return redirect("polls:login")
      messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="polls/register.html", context={"register_form":form})



def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("polls:index")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="polls/login.html", context={"login_form":form})