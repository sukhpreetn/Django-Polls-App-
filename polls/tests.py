from django.test import TestCase
import datetime

from django.urls import reverse
from django.utils import timezone
from django.test import TestCase

from .models import Question

# Create your tests here.
# 3 Create a Question with a pub_date in the future
'''
import datetime
from django.utils import timezone
from polls.models import Question
future_question = Question(pub_date=timezone.now() + datetime.timedelta(days=30))
future_question.was_published_recently()
Returns true even though that doesn't make sense
'''


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

# models test

# 4 TestCase runs tests without effecting your data
# by creating a temporary database for testing
class QuestionMethodTests(TestCase):

    # 4 Put the code used in the shell here
    # Start the method name with test
    def test_was_published_recently_with_future_question(self):
        # 4 Create a time 30 days in the future
        time = timezone.now() + datetime.timedelta(days=30)

        # 4 Create a question using the future time
        future_question = Question(pub_date=time)

        # 4 Check to see if the output is False like we expect
        self.assertIs(future_question.was_published_recently(), False)

        # 4 Run the test in the terminal
        # python3 manage.py test polls
        # You'll see that the test failed

        # 4 Fix the bug in models.py

    # 6 Return false if pub_date is older then 1 day

    def test_was_published_recently_with_old_question(self):
        # Should return false if pub_date is older then 1 day
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    # 6 Return True if published within the last day

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(),True)





######## View tests

        class QuestionViewTests(TestCase):

            # 10 Test to see what happens if there are no questions
            def test_index_view_with_no_questions(self):
                # Get the client
                response = self.client.get(reverse('polls:index'))

                # Check the status code
                self.assertEqual(response.status_code, 200)

                # Verify that response contains this string
                self.assertContains(response, "No polls are available.")

                # Check if latest_question_list is empty
                self.assertQuerysetEqual(response.context['latest_question_list'], [])

            # 10 Make sure questions with a pub_date in past are shown
            def test_index_view_with_a_past_question(self):
                # Create sample question
                create_question(question_text="Past question.", days=-30)

                # Get client
                response = self.client.get(reverse('polls:index'))

                # Verify that the question shows
                self.assertQuerysetEqual(
                    response.context['latest_question_list'],
                    ['<Question: Past question.>']
                )

            # 10 Make sure questions with future pub_date don't show
            def test_index_view_with_a_future_question(self):
                # Create question
                create_question(question_text="Future question.", days=30)

                # Get client
                response = self.client.get(reverse('polls:index'))

                # Verify response contains text
                self.assertContains(response, "No polls are available.")

                # Verify that latest_question_list is empty
                self.assertQuerysetEqual(response.context['latest_question_list'], [])

            # 10 Verify that if past and future questions exist that only
            # past show
            def test_index_view_with_future_question_and_past_question(self):
                # Create questions
                create_question(question_text="Past question.", days=-30)
                create_question(question_text="Future question.", days=30)

                # Get client
                response = self.client.get(reverse('polls:index'))

                # Verify that question list only contains past questions
                self.assertQuerysetEqual(
                    response.context['latest_question_list'],
                    ['<Question: Past question.>']
                )

            # 10 Make sure question list shows multiple questions
            def test_index_view_with_two_past_questions(self):
                # Create questions
                create_question(question_text="Past question 1.", days=-30)
                create_question(question_text="Past question 2.", days=-5)

                # Create client
                response = self.client.get(reverse('polls:index'))

                # Verify that both questions show
                self.assertQuerysetEqual(
                    response.context['latest_question_list'],
                    ['<Question: Past question 2.>', '<Question: Past question 1.>']
                )



# urls tests

class QuestionIndexDetailTests(TestCase):

    # 13 Make sure future question detail pages show 404
    def test_detail_view_with_a_future_question(self):
        # Create question
        future_question = create_question(question_text='Future question.', days=5)

        # Open url using the future question in the url
        url = reverse('polls:detail', args=(future_question.id,))

        # Get client response
        response = self.client.get(url)

        # Verify that it returns 404
        self.assertEqual(response.status_code, 404)

    # 13 Verify that past questions show in detail
    def test_detail_view_with_a_past_question(self):
        # Create question
        past_question = create_question(question_text='Past Question.', days=-5)

        # Open url with past question
        url = reverse('polls:detail', args=(past_question.id,))

        # Get response
        response = self.client.get(url)

        # Verify the question shows
        self.assertContains(response, past_question.question_text)

