from django.shortcuts import render, get_object_or_404
from .models import Question, Choice
from django.template import loader
from django.http import HttpResponse


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    lastest_choice_list = Choice.objects.order_by("-choice_text")
    context = {
        "latest_question_list": latest_question_list,
        "lastest_choice_list": lastest_choice_list,
    }
    return render(request, "polls/index.html", context)

def question(request):
    lastest_question_list = Question.objects.order_by("-pub_date")[:5]
    output = " <br> ".join([q.question_text for q in lastest_question_list])
    return HttpResponse(output)
def choices(request):
    lastest_choice_list = Choice.objects.order_by("-choice_text")
    output = " <br> ".join([q.choice_text for q in lastest_choice_list])
    return HttpResponse(output)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id,)
    return render(request, "polls/detail.html", {"question": question , "data":  question.pub_date })

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)