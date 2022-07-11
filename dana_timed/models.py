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


doc = """
This is the Dana task.
"""


class Constants(BaseConstants):
    name_in_url = 'dana_timed'
    players_per_group = None
    num_rounds = 1
    timer = 30  # in seconds
    dana2A_self = 10
    dana2A_other = 0
    dana2B_self = 5
    dana2B_other = 15


class Subsession(BaseSubsession):
    def creating_session(self):
        pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    store_time = models.FloatField()  # for the timer
    danat = models.StringField(blank=True)  # whether participant takes selfish choice in Dana timed task
    payoff2_self_danat = models.IntegerField()  # payoff dana_timed
    payoff2_charity_danat = models.IntegerField()  # payoff dana_timed
    q1 = models.StringField(label='Could you give reasons for your previous decision?', initial='')
    q_diff = models.IntegerField(widget=widgets.RadioSelectHorizontal,initial='',
                                 label="How difficult was it to reconsider Task 3",
                                 choices=[[1, "Very difficult"], [2, "Difficult"], [3, "Not difficult"], [4, "Easy"], [5, "Very easy"]])


    def set_payoffs2(self):
        if self.danat == "A":
            self.payoff2_self_danat = 10#Constants.dana2A_self
            self.payoff2_charity_danat = 0 #Constants.dana2A_other
        elif self.danat == "B":
            self.payoff2_self_danat = 5#Constants.dana2B_self
            self.payoff2_charity_danat = 15 #Constants.dana2B_other
        # to store for next app (button task + final payoffs)
        self.participant.vars["payoff2_self_danat"] = self.payoff2_self_danat
        self.participant.vars["payoff2_charity_danat"] = self.payoff2_charity_danat
