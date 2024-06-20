from django.test import TestCase

# Create your tests here.
import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question, Choice

class QuestionModelTeste(TestCase):
    def test_was_published_recently_with_future_question(self):
        """ """
        time =timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)
        
    def test_was_published_with_recent_question(self):
        """RETORNAR True CASO O A QUESTION ESTIVER NO ULTIMO DIA"""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59 ,seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
def create_question(question_text, days):
    """"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)
    
class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """ SE A QUESTION NAO EXISTE """  
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
Perguntas com pub_date no passado são exibidas no
página de índice."""
        question = create_question(question_text="Questão anterios", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "Sem pesquisa disponivel. ")
        self.assertQuerySetEqual(response.context["latest_question_list"], [question],
                                 )
    def test_future_question(self):
        """

Perguntas com uma pub_date no futuro não são exibidas na página inicial."""
        question = create_question(question_text="Questão futura", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "Sem pesquisa disponivel. ")
        self.assertQuerySetEqual(response.context["latest_question_list"], [],
                                 )
    def test_past_question_and_future_question(self):
        """

Perguntas com uma pub_date no futuro não são exibidas na página inicial."""
        create_question(question_text="Questão futura", days=30)
        question = create_question(question_text="Questão Anterior", days=-30)
        response = self.client.get(reverse("polls:index"))
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "Sem pesquisa disponivel. ")
        self.assertQuerySetEqual(response.context["latest_question_list"], [question],
                                 )
    def test_two_past_question(self):
        """A question index page may display multiple question"""
        question1 = create_question(question_text="Questão anterior 1.", days=-30)
        question2 = create_question(question_text="Questão anterior 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question1, question2],)


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):    
        """ The detail od a question with  a pub_date in the future returns a 404 not found"""
        future_question = create_question(question_text="Questão futura", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """"""
        past_question = create_question(question_text="Questão anterior", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)