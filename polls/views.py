# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic
from django.contrib import messages

from .models import Question, Choice


# class IndexView(generic.ListView):
#     template_name = 'polls/index.html'
#     context_object_name = 'latest_question_list'

#     def get_queryset(self):
#         """
#         Return the last five published questions (not including those set to be
#         published in the future).
#         """
#         return Question.objects.filter(
#             pub_date__lte=timezone.now()
#         ).order_by('-pub_date')[:5]

def index(request):
    """Display all questions in the system according to publication date.

    Returns:
    HttpResponseObject -- index page

    """
    all_question = Question.objects.all().order_by('-pub_date')

    return render(request, 'polls/index.html', {'latest_question_list': all_question})


# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'polls/detail.html'

#     def get_queryset(self):
#         """
#         Excludes any questions that aren't published yet.
#         """
#         return Question.objects.filter(pub_date__lte=timezone.now())

def detail(request, pk):
    """Display the detail of selected questions.

    Returns:
    HttpResponseObject -- detail page

    """
    question = get_object_or_404(Question, pk=pk)
    if not question.can_vote():
        messages.error(request, "You can't vote on this question")
        return redirect('polls:index')
    else:
        return render(request, 'polls/detail.html', {'question': question})


class ResultsView(generic.DetailView):
    """Generic view that uses a template called polls/result.html."""

    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    """Display the vote result of selected questions.

    Returns:
    HttpResponseObject -- vote page

    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        messages.error(request, "You didn't select a choice.")
        return render(request, 'polls/detail.html', {
            'question': question,
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
