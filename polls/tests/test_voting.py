# Create your tests here.
import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from polls.models import Question
from django.urls import reverse


def create_question(question_text, start_days, end_days):
    """
    Create a question with the given `question_text`.

    Published the given number of `days` offset to now

    Negative for questions published in the past

    Positive for questions that have yet to be published

    """
    start_time = timezone.now() + datetime.timedelta(days=start_days)
    end_time = timezone.now() + datetime.timedelta(days=end_days)

    return Question.objects.create(question_text=question_text, pub_date=start_time, end_date=end_time)


class VoteModelTests(TestCase):
    """Test for Vote Model."""

    def setUp(self):
        """Initialize the question with choices and a user."""
        self.question = Question.objects.create(
            question_text='Select a number',
            pub_date=timezone.now(),
            end_date=timezone.now() + datetime.timedelta(days=7)
        )
        self.question.choice_set.create(choice_text='1')
        self.user = {
            'username': 'minion12',
            'password': 'banana123'
        }
        User.objects.create_user(**self.user)

    def test_authenticated_vote(self):
        """If the user is authenticated, he or she can vote."""
        self.client.post(reverse('login'), self.user)
        url = reverse('polls:vote', args=(self.question.id,))
        response2 = self.client.get(url)
        self.assertEqual(response2.status_code, 200)  # the authenticated user can go to vote page.

        # submit vote
        response = self.client.post(url, {'choice': '1'})
        self.assertTrue(self.question.vote_set.filter(question=self.question).exists)
        self.assertEqual(response.status_code, 302)  # if vote is success redirect to result page

    def test_unauthenticated_vote(self):
        """If the user is not authenticated, he or she can't vote."""
        url = reverse('polls:vote', args=(self.question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # unauthenticated to login page
