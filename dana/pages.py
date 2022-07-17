from ._builtin import Page
from .models import *
from .stuff import UnderstandingQuestionsPage

class InstructionsTask1(Page):
    form_model = 'player'


class Task1(Page):
    form_model = 'player'
    form_fields = ['task1','timeSpent']

    def before_next_page(self):
        self.player.set_payoffs1()
        payoff1_self = self.player.payoff1_self
        payoff1_charity = self.player.payoff1_charity

class Task1Check1(UnderstandingQuestionsPage):
    set_correct_answers = False
    form_model = 'player'
    form_field_n_wrong_attempts = 'understanding_questions_wrong_attempts'
    template_name = 'dana/UnderstandingQuestionsPage.html'

    def get_questions(self):
        return self.player.get_questions_method()

    def before_next_page(self):
        self.player.store_uq_dana()

page_sequence = [
    InstructionsTask1,
    Task1Check1,
    Task1,

]
