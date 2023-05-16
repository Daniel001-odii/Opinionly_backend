from django.db import models
from django.utils import timezone
import datetime
from django.contrib import admin

from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)

    question_title = models.CharField(max_length=200)
    question_description = models.TextField(blank=True, default = "no description ")
    slug = models.SlugField(unique=True, blank=True)
    pub_date = models.DateTimeField("date published",auto_now_add=True)
    views = models.IntegerField(default=0)
    """
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.question_title)
        super().save(*args, **kwargs)
    """
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.question_title)
            slug = base_slug
            counter = 1
            while Question.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
        
        

    def __str__(self):
        return self.question_title
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
    downvotes = models.ManyToManyField(User, related_name='downvoted_choices', blank=True, default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text