

# Create your tests here.
import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question
from django.urls import reverse
import unittest


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


class QuestionModelTests(TestCase):
    """Test for Question Model."""

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        """is_published() returns False for questions that is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_is_published_with_past_question(self):
        """is_published() returns True for questions that is in the past."""
        time = timezone.now() + datetime.timedelta(days=-30)
        past_question = Question(pub_date=time)
        self.assertIs(past_question.is_published(), True)

    def test_is_published_with_recent_question(self):
        """is_published() returns True for questions that is within the last day."""
        time = timezone.now() + datetime.timedelta(hours=-3)
        recent_question = Question(pub_date=time, end_date=time + datetime.timedelta(days=1))
        self.assertIs(recent_question.is_published(), True)

    def test_can_vote_with_future_question(self):
        """can_vote() returns False for question that is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.can_vote(), False)

    def test_can_vote_with_past_question(self):
        """can_vote() returns False for question that is in the past."""
        time = timezone.now() + datetime.timedelta(days=30)
        past_question = Question(pub_date=time)
        self.assertIs(past_question.can_vote(), False)

    def test_can_vote_with_recent_question(self):
        """can_voted() returns True for question that is within the last day."""
        time = timezone.now() + datetime.timedelta(hours=-3)
        recent_question = Question(pub_date=time, end_date=time + datetime.timedelta(days=1))
        self.assertIs(recent_question.can_vote(), True)


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


if __name__ == "__main__":
    unittest.main(verbosity=2)
