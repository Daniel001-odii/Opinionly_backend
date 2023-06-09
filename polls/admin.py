from django.contrib import admin
from .models import Question, Choice
# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ["question_text"]
    list_filter = ["pub_date", "posted_by"]
    list_display = ["question_title", "slug", "pub_date", "was_published_recently"]
    fieldsets = [
        (None, {"fields": ["question_title", "question_description"]}),
        #("Date information", {"fields": , "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)