# Create your tests here.
import datetime

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


class QuestionIndexViewTests(TestCase):
    """Tests for Question Index View."""

    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """Questions with a pub_date in the past are displayed on the index page."""
        create_question(question_text="Past question.", start_days=-5, end_days=-2)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """Questions with a pub_date in the future aren't displayed on the index page."""
        future_question = create_question(question_text="Future question.", start_days=3, end_days=5)
        response = self.client.get(reverse('polls:index'))
        self.assertIs(future_question.can_vote(), False)
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Future question.>'])

    def test_future_question_and_past_question(self):
        """Even if both past and future questions exist, only past questions are displayed."""
        past_question = create_question(question_text="Past question.", start_days=-5, end_days=-3)
        future_question = create_question(question_text="Future question.", start_days=3, end_days=5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Future question.>', '<Question: Past question.>'],
        )
        self.assertIs(past_question.can_vote(), False)
        self.assertIs(future_question.can_vote(), False)

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        create_question(question_text="Past question 1.", start_days=-5, end_days=-3)
        create_question(question_text="Past question 2.", start_days=-4, end_days=-2)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )
