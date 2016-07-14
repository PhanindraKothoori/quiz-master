from django.conf.urls import url, include

import quiz
from quiz import views, classviews

urlpatterns=[


    url(r'home/',view=classviews.ExamListView.as_view(),name='home'),
    url(r'newexam/',view=classviews.ExamCreateView.as_view(),name='newexam'),
    url(r'editexam/(?P<pk>[0-9]+)',view=classviews.ExamUpdateView.as_view(),name='editexam'),
    url(r'deleteexam/(?P<pk>[0-9]+)',view=classviews.ExamDeleteView.as_view(),name='deleteexam'),

    # here the primary key refers to the foreign key of the exam to which the question belongs to
    url(r'newquestion/(?P<pk>[0-9]+)',view=classviews.QuestionCreateView.as_view(),name='newquestion'),
    url(r'changequestions/(?P<pk>[0-9]+)',view=classviews.QuestionsEditView.as_view(),name='changequestions'),
    # here the primary key refers to the ID of itself
    url(r'editquestion/(?P<pk>[0-9]+)',view=classviews.QuestionEditView.as_view(),name='editquestion'),
    url(r'deletequestion/(?P<pk>[0-9]+)',view=classviews.QuestionDeleteView.as_view(),name='deletequestion'),
    url(r'allquestions',view=classviews.QuestionListView.as_view(),name='allquestions'),

    url(r'write/(?P<pk>[0-9]+)',view=classviews.WriteExam.as_view(),name='write'),
]