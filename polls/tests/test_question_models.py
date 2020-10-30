import datetime
from django.test import TestCase

from django.utils import timezone

from polls.models import Question


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
