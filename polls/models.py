from django.db import models
from django.utils import timezone
import datetime
from django.contrib import admin

from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)

    question_text = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    pub_date = models.DateTimeField("date published",auto_now_add=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.question_text)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question_text
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    upvotes = models.ManyToManyField(User, related_name='upvoted_choices', blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text