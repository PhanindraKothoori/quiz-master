from django import forms
from django.contrib.auth.models import User

from quiz.models import Exam, Question


class ExamForm(forms.ModelForm):
    class Meta:
        model=Exam
        fields=['name','length','questioncount']


class QuestionForm(forms.ModelForm):
    option1=forms.ChoiceField()
    option2=forms.ChoiceField()
    option3=forms.ChoiceField()
    option4=forms.ChoiceField()

    class Meta:
        model=Question
        fields=['text','option1','option2','option3','option4','correctoption','exam']


class Userform(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','email','first_name','last_name','password']