def addChoice(request):
        if method == 'POST':
            choice_form = ChoiceForm(request.POST)
            if choice_form.is_valid():
                choice = choice_form.save(commit=False)
                choice.question = question
                choice.save()
                return HttpResponseRedirect(reverse("polls:index"))
        else:
            choice_form = ChoiceForm()
        return render(request, 'polls/detail.html', {'choice_form': choice_form})
    
    
    <!-- <li><a href="{% url 'polls:detail' slug=question.slug %}">{{ question.question_text }}</a></li>-->
    
 from django.db import models
from django.contrib.auth.models import User

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    

    def __str__(self):
        return self.choice_text

from django.shortcuts import render
from django.db.models import Max
from .models import Question

def poll_list(request):
    questions = Question.objects.annotate(max_votes=Max('choice__votes')).filter(choice__votes=F('max_votes'))
    
    return render(request, 'polls/poll_list.html', {'questions': questions})


from django.shortcuts import render
from django.db.models import Max
from .models import Question

def poll_list(request):
    questions = Question.objects.annotate(max_votes=Max('choice__votes')).filter(choice__votes=F('max_votes'))
    
    return render(request, 'polls/poll_list.html', {'questions': questions})
