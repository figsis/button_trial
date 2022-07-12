from ._builtin import Page
from .models import *


class InstructionsTask1(Page):
    form_model = 'player'


class Task1(Page):
    form_model = 'player'
    form_fields = ['task1','timeSpent']

    def before_next_page(self):
        self.player.set_payoffs1()
        payoff1_self = self.player.payoff1_self
        payoff1_charity = self.player.payoff1_charity


page_sequence = [

    InstructionsTask1,
    Task1,
    # SummaryTask1
]
