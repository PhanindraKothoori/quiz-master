import site
from django.contrib import admin

# Register your models here.
from quiz.models import Question, Exam

admin.site.register([Question,Exam])