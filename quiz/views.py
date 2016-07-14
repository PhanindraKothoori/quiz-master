from django.contrib.auth import logout
from django.forms.formsets import formset_factory
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from quiz.forms import ExamForm, QuestionForm


def index(request):
    return HttpResponse(render(request,template_name='index.html'))

def logoutuser(request):
    logout(request)
    return redirect('/login/')