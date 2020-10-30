import datetime
from django.test import TestCase

from django.urls import reverse
from django.utils import timezone

from polls.models import Question


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


class QuestionDetailViewTests(TestCase):
    """Tests for Question Detail View."""

    def test_future_question(self):
        """The detail view of a question with a pub_date in the future returns a 302 temporary redirect."""
        future_question = create_question(question_text='Future question.', start_days=3, end_days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past displays the question's text."""
        past_question = create_question(question_text='Past Question.', start_days=-5, end_days=-3)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
