# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic
from django.contrib import messages

from mysite.settings import LOGGING
from .models import Question, Choice
import logging.config

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('my_logger')


def index(request):
    """Display all questions in the system according to publication date.

    Returns:
    HttpResponseObject -- index page

    """
    # Return an 'invalid login' error message.
    all_question = Question.objects.all().order_by('-pub_date')

    return render(request, 'polls/index.html', {'latest_question_list': all_question})


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
        user_vote = question.vote_set.get(user=request.user)
        return render(request, 'polls/detail.html', {'question': question, 'vote': user_vote})


class ResultsView(generic.DetailView):
    """Generic view that uses a template called polls/result.html."""

    model = Question
    template_name = 'polls/results.html'


@login_required(login_url='/accounts/login/')
def vote(request, question_id):
    """Display the vote result of selected questions.

    Returns:
    HttpResponseObject -- vote page

    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        logger.info(
            '{user} voted on {question} (id = {id})'.format(user=request.user, question=question, id=question.id))
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        messages.error(request, "You didn't select a choice.")
        return render(request, 'polls/detail.html', {
            'question': question,
        })
    else:
        previous_choice = question.vote_set.all()
        if previous_choice:
            previous_vote = question.vote_set.get(question=question, user=request.user)
            previous_vote.choice = selected_choice
            previous_vote.save()
        else:
            selected_choice.vote_set.create(question=question, user=request.user)

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def get_client_ip(request):
    """Get the visitor’s actual IP address."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(user_logged_in)
def on_login(user, request, **kwargs):
    """Log message of login at info level including username and IP address."""
    logger.info(f'IP: {get_client_ip(request)} {user} just logged in.')


@receiver(user_logged_out)
def on_logout(user, request, **kwargs):
    """Log message of logout at info level including username and IP address."""
    try:
        logger.info(f'IP: {get_client_ip(request)} {user.username} has logged out.')
    except AttributeError:
        logger.info(f'IP: {get_client_ip(request)} has logged out.')


@receiver(user_login_failed)
def login_fail(credentials, request, **kwargs):
    """Log message of fail login attempt at warning level including username and IP address."""
    logger.warning(f"IP: {get_client_ip(request)} Fail to log in for {credentials['username']}")
