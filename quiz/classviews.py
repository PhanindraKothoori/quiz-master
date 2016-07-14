import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.forms.formsets import formset_factory
from django.http.response import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from mainproject.settings import LOGIN_REDIRECT_URL
from quiz.forms import Userform, QuestionForm
from quiz.models import Exam, Question

@method_decorator(login_required,'dispatch')
class ExamCreateView(CreateView):
    model = Exam
    fields = ['name','length','questioncount']
    template_name = 'quiz/newexam.html'
    success_url = '/quiz/newquestion/'

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(ExamCreateView, self).form_valid(form)

    def get_success_url(self):
        return self.success_url+str(self.object.id)

@method_decorator(login_required,'dispatch')
class ExamListView(ListView):
    model = Exam
    template_name = 'home.html'

    def get_queryset(self):
        return Exam.objects.all()

@method_decorator(login_required,'dispatch')
class ExamUpdateView(UpdateView):
    model = Exam
    fields = ['name', 'length', 'questioncount']
    success_url = '/quiz/newquestion/'
    examid=None

    def get_object(self, queryset=None):
        obj = Exam.objects.get(id=self.kwargs.get('pk'))
        if obj.user!=self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        self.examid=self.kwargs['pk']
        if Question.objects.filter(exam_id=self.examid).count() == Exam.objects.get(id=self.examid).questioncount:
            return '/quiz/home/'
        else:
            return super(ExamUpdateView, self).get_success_url() + str(self.examid)

@method_decorator(login_required,'dispatch')
class ExamDeleteView(DeleteView):
    model = Exam
    fields = ['name', 'length', 'questioncount']
    success_url = '/quiz/home/'

    def get_object(self, queryset=None):
        obj = Exam.objects.get(id=self.kwargs.get('pk'))
        if obj.user != self.request.user:
            raise Http404
        return obj

@method_decorator(login_required,'dispatch')
class QuestionCreateView(CreateView):
    model = Question
    template_name = 'quiz/newquestion.html'
    fields = ['text','option1','option2','option3','option4','correctoption','exam']
    success_url = '/quiz/newquestion/'
    examid=None

    def get_context_data(self, **kwargs):
        self.examid=self.kwargs['pk']
        if self.request.method=='GET':
            kwargs.update({'examid':self.examid})
        return super(QuestionCreateView, self).get_context_data(**kwargs)

    def get_form(self, form_class=None):
        form = super(QuestionCreateView, self).get_form(form_class)
        if self.examid:
            form.fields['exam'].queryset=Exam.objects.filter(id=self.examid)
        else:
            self.examid=self.kwargs['pk']
        return form

    def form_valid(self, form):
        return super(QuestionCreateView, self).form_valid(form)

    def get_success_url(self):
        if Question.objects.filter(exam_id=self.examid).count()==Exam.objects.get(id=self.examid).questioncount:
            return '/quiz/home/'
        else:
            return super(QuestionCreateView, self).get_success_url()+str(self.examid)

@method_decorator(login_required,'dispatch')
class QuestionEditView(UpdateView):
    model = Question
    fields = ['text','option1','option2','option3','option4','correctoption','exam']
    success_url = 'quiz/home/'

@method_decorator(login_required,'dispatch')
class QuestionDeleteView(DeleteView):
    model = Question
    success_url = 'quiz/listquestions/'

@method_decorator(login_required,'dispatch')
class QuestionListView(ListView):
    model = Question
    template_name = 'allquestions.html'

@method_decorator(login_required,'dispatch')
class QuestionsEditView(ListView):
    model = Question
    template_name = 'allquestions.html'
    examid=None
    queryset = None

    def get_context_data(self, **kwargs):
        self.examid=self.kwargs['pk']
        self.queryset=Question.objects.filter(exam_id=int(self.examid))
        return super(QuestionsEditView, self).get_context_data(**kwargs)

    def get_queryset(self):
        return super(QuestionsEditView, self).get_queryset()


@method_decorator(login_required,'dispatch')
class WriteExam(View):
    form_class=QuestionForm
    template_name='quiz/write.html'
    examid=None


    def get(self,request,**kwargs):
        self.examid=int(self.kwargs['pk'])
        queryset=Question.objects.filter(exam_id=int(self.examid))
        jsonset=serializers.serialize('json',queryset=queryset,fields=('text','option1','option2','option3','option4'))
        # jsonset=json.dumps(queryset)
        return HttpResponse(render(request,context={'formset':queryset, 'jsonset':jsonset},template_name='quiz/write.html'))

    def post(self,request,**kwargs):
        def dict_compare(d1, d2):
            d1_keys,d2_keys = set(d1.keys()),set(d2.keys())
            intersect_keys = d1_keys.intersection(d2_keys)
            same = set(o for o in intersect_keys if d1[o] == d2[o])
            return same

        self.examid=int(self.kwargs['pk'])
        answers=dict((int(key[-1]),int(value)) for (key,value) in request.POST.items() if str(key[-1]).isdigit())
        correctanswers=Question.objects.filter(exam_id=self.examid).values_list('correctoption')
        import itertools
        correctanswers=dict(enumerate(list(itertools.chain.from_iterable(correctanswers)),1))
        score=(dict_compare(answers,correctanswers))
        return HttpResponse(render(request,'quiz/done.html',context={'score':len(score),'attempted':len(answers),'correctlyanswered':list(score)}))

class UserSignInView(View):
    form_class=Userform
    template_name='registration/signup.html'

    def get(self, request):
        if self.request.user.is_anonymous():
            form = self.form_class(None)
            return render(request, template_name=self.template_name, context={'form': form})
        else:
            return redirect('/quiz/home/')

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # clean the data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            firstname = form.cleaned_data['first_name']
            lastname = form.cleaned_data['last_name']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(LOGIN_REDIRECT_URL)

        return render(request, self.template_name, {'form': form})