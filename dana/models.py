from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

import random

doc = """
This is the Dana task.
"""


class Constants(BaseConstants):
    name_in_url = 'dana'
    players_per_group = None
    num_rounds = 1
    # Dana payoffs
    danaA_self = 10
    danaB_self = 3
    danaA_other = 0
    danaB_other = 15


class Subsession(BaseSubsession):
    pass



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    timeSpent = models.FloatField()
    task1 = models.StringField(blank=True)  # whether participant takes selfish choice in Dana task
    payoff1_self = models.IntegerField()  # payoff task 1 (dana)
    payoff1_charity = models.IntegerField()  # payoff task 1 (dana)
    browser = models.StringField()
    understanding_questions_wrong_attempts = models.PositiveIntegerField()  # for all tasks
    uq_wrong_dana = models.PositiveIntegerField()  # storing UQ Dana

    def set_payoffs1(self):   # payoffs Task 1 (Dana)
        if self.task1 == "A":
            self.payoff1_self = Constants.danaA_self
            self.payoff1_charity = Constants.danaA_other
        elif self.task1 == "B":
            self.payoff1_self = Constants.danaB_self
            self.payoff1_charity = Constants.danaB_other
        # to store for next app (button task + final payoffs)
        self.participant.vars["payoff1_self"] = self.payoff1_self
        self.participant.vars["payoff1_charity"] = self.payoff1_charity
        self.participant.vars["task1"] = self.task1

    def store_uq_dana(self):
        self.uq_wrong_dana = self.understanding_questions_wrong_attempts

    def get_questions_method(self):
        questions = [
            {
                'question': 'In the table my bonus payment is denoted in',
                'options': ['Red', 'Blue'],
                'correct': 'Blue',
            },
            {
                'question': 'If you choose A, the Red Cross obtains a bonus of',
                'options': ['5 pounds', '10 pounds', '7 pounds'],
                'correct': '5 pounds',
            },
            {
                'question': 'If you choose B, you earn a bonus of',
                'options': ['5 pounds', '7 pounds', '10 pounds'],
                'correct': '7 pounds',
            },

        ]
        return questions


