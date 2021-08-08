from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from .models import Question,Choice
from django.template import loader
from django.urls import reverse
from django.shortcuts import get_object_or_404,render
from django.views import generic
from datetime import timedelta,timezone
import datetime
from django.utils import timezone

# Create your views here.


#this is old index view
# def index(request):
#     latest_question_list= Question.objects.order_by('-pub_date')[:5]
#     # output=', '.join([q.question_text for q in latest_question_list])
#     # template=loader.get_template('polls/index.html')
#     context={
#         'latest_question_list':latest_question_list,
#     }
#     # return HttpResponse(template.render(context,request))
#     return render(request,'polls/index.html',context)

#creating generin index use as per django _------------------->

class IndexView(generic.ListView):
    template_name='polls/index.html'
    context_object_name='latest_question_list'

    def get_queryset(self):
        """ Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]





#this is old detail view------------------------------------------------
# def detail(request,question_id):
#     # try:
#     #     question=Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Quetstion does not exist")
#     question=get_object_or_404(Question,pk=question_id)
#     return render(request,'polls/detail.html',{'question':question})

#this is generic detail view as ver django--------------------------------------------

class DetailView(generic.DetailView):
    model=Question
    template_name='polls/detail.html'
    def get_queryset(self):
        """
        excludes any quastions that aren't published yet
        """
        return Question.objects.filter(pub_date__lte=timezone.now())




#this is old result view-------------------------------------
# def results(request,question_id):
#     question=get_object_or_404(Question,pk=question_id)
#     return render(request,'polls/result.html',{'question': question})

#this is generic detail view as per django---------------------------------

class ResultsView(generic.DetailView):
    model=Question
    template_name='polls/result.html'



def vote(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request,'polls/detail.html',{
            'question':question,
            'error_message':"you didnt select a choice",
        })
    else:
        selected_choice.votes +=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def was_published_recently(self):
    now=timezone.now()
    return now - datetime.timedelta(days=1) <= self.pub_date <= now



    

