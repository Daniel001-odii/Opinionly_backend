from django import forms
from .models import Question, Choice
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class QuestionForm(forms.ModelForm):
    class Meta:
      model = Question
      fields = ['question_title', 'question_description']
    def __init__(self, *args, **kwargs):
      self.user = kwargs.pop("user", None)
      super().__init__(*args, **kwargs)

    def save(self, commit=True):
      question = super().save(commit=False)
      if self.user:
          question.posted_by = self.user
      if commit:
          question.save()
      return question
    
    
    
    
class ChoiceForm(forms.ModelForm):
    class Meta:
      model = Choice
      fields = ['choice_text']





# Create your forms here.
#for user registration.....
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
      model = User
      fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
      user = super(NewUserForm, self).save(commit=False)
      user.email = self.cleaned_data['email']
      if commit:
        user.save()
      return user