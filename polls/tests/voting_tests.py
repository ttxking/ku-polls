
# Create your tests here.
import datetime

from django.test import TestCase
from django.utils import timezone

from polls.models import Question
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


class VoteModelTests(TestCase):
    """Test for Vote Model."""
