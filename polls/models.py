from django.db import models
from django.utils import timezone
import datetime


# Create your models here.

class Question(models.Model):
    """A Question model that has a question, a publication date and an end date."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('data published')
    end_date = models.DateTimeField('end date')

    def __str__(self):
        """Return question with question text."""
        return self.question_text

    def was_published_recently(self):
        """Return True if question is published within 1 day."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Return True if question is already published."""
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """Return True if question can be voted."""
        return self.pub_date <= timezone.now() <= self.end_date

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    """A Choice model has two fields: the text of the choice and a vote tally.

    Each Choice is associated with a Question.

    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return choice text of each choice."""
        return self.choice_text
