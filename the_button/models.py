
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

from otree.api import *
import random

#from django import forms

doc = """
This is the button game. 
"""


class Constants(BaseConstants):
    name_in_url = 'the_button'
    num_rounds = 1
    players_per_group=None
    # Button payoffs
    optionA = [3, 15]  # bonus payments NO CLICK [receiver, charity]
    optionB = [10, 0]  # bonus payment CLICK
    optionA0 = optionA[0]
    optionA1 = optionA[1]
    optionB0 = optionB[0]
    optionB1 = optionB[1]
    timer = 180 # in seconds
    dana2A_self = 10
    dana2A_other = 0
    dana2B_self = 3
    dana2B_other = 15
    numberList = [1, 0]

class Subsession(BaseSubsession):
    def creating_session(self):
        for player in self.get_players():
            player.selected = random.choices(Constants.numberList, weights=(10,90), k=1)[0] #10,90
            self.session.vars["selected"] = player.selected
            player.treatment = random.choices(["ButtonA", "ButtonB", "NoButton"], weights=(40,40,20), k=1)[0] #10,90
            player.participant.vars["treatment"] = player.treatment
            player.participant.vars["payoff3"] = ""
            player.participant.vars["bonus"] = ""



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.StringField()
    button = models.BooleanField(initial=0)
    bonus = models.FloatField()
    store_time = models.FloatField()  # for the timer
    store_timeA = models.FloatField()
    store_timeB = models.FloatField()
    payoff2_self = models.IntegerField()  # payoff task 2 (button)
    payoff3 = models.FloatField()
    payoff4 = models.FloatField()
    payoff2_charity = models.IntegerField()  # payoff task 2 (button)
    danat = models.StringField(blank=True)  # whether participant takes selfish choice in Dana timed task
    secondary_button = models.StringField()
    payoff2_self_danat = models.IntegerField()  # payoff dana_timed
    payoff2_charity_danat = models.IntegerField()  # payoff dana_timed
    # How strong was the temptation to press the button?
    q0 = models.IntegerField(label='How strong was the temptation to press the button? (0: not tempting at all, 10: very tempting) ', choices=[0,1, 2, 3, 4, 5, 6, 7, 8, 9,10],
        widget=widgets.RadioSelectHorizontal)
    #Reasons to press
    q1 = models.LongStringField(label='Why did you decide to press the button?')
    q2 = models.LongStringField(label='Why did you decide not to press the button?')
    #Why did you change/did not change your final decision? In all treatments every time a discrepancy between decisions.
    q_change = models.LongStringField(label='Why did you change your mind when you were given more time to think about the decision in Task 3?')
    q_nochange = models.LongStringField(label='Why did you not change your mind when you were given more time to think about the decision in Task 3?')
    #What was the highest number that you saw appear on screen?
    q_number = models.IntegerField(label="What was the highest number that you saw appearing on screen?")
    selected = models.IntegerField()
    q_feedback = models.LongStringField(label="This is the end of the survey. "
                                            "In case you have comments, please leave them here.",
                                      blank=True)
    q_feedback_pilot = models.LongStringField(label="If you found any instructions unclear or confusing, please let us know here.",
                                            blank=True)

    def set_payoffs(self):
        if self.treatment == "ButtonA":
            if self.store_time != 0:
                self.payoff2_self = Constants.optionB[0]
                self.payoff2_charity = Constants.optionB[1]
            elif self.store_time == 0:
                self.payoff2_self = Constants.optionA[0]
                self.payoff2_charity = Constants.optionA[1]
        elif self.treatment == "ButtonB":
            if self.store_time != 0:#pressing the button yields the altruistic action
                self.payoff2_self = Constants.optionA[0]
                self.payoff2_charity = Constants.optionA[1]
            else: #not pressing the button yields the selfish action
                self.payoff2_self = Constants.optionB[0]
                self.payoff2_charity = Constants.optionB[1]
        elif self.treatment == "NoButton":
            if self.secondary_button == "A":
                self.payoff2_self_danat = 10
                self.payoff2_charity_danat = 0
            elif self.secondary_button == "B":
                self.payoff2_self_danat = 3
                self.payoff2_charity_danat = 15


    def set_bonus(self):
        if self.q_number == 100:
            self.participant.vars["bonus"] = 0.1
            self.bonus = self.participant.vars["bonus"]
        elif self.q_number != 100:
            self.bonus = 0


    def set_payoff3(self):
        if self.selected == 1:
            if self.store_time != 0:
                if self.treatment == "ButtonA":  #treatment A and press
                    if self.q_number == 100:
                        self.payoff3 = 10.1
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                    elif self.q_number != 100:
                        self.payoff3 = 10
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                elif self.treatment == "ButtonB":  # treatment B and press
                    if self.q_number == 100:
                        self.payoff3 = 3.1
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                    elif self.q_number != 100:
                        self.payoff3 = 3
                        self.payoff4 = self.payoff3+ float(self.participant.vars["payoff_svo"])
            else: #button not pressed
                if self.treatment == "ButtonA": #treatment A and not press
                    if self.q_number == 100:
                        self.payoff3 = 3.1
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                    elif self.q_number != 100:
                        self.payoff3 = 3
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                elif self.treatment == "ButtonB":  # treatment B and  not press
                    if self.q_number == 100:
                        self.payoff3 = 10.1
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                    elif self.q_number != 100:
                        self.payoff3 = 10
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
        elif self.selected == 0:
            if self.store_time != 0:
                if self.treatment == "ButtonA": # treatment A and press
                    if self.q_number == 100:
                        self.payoff3 = 0.1
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                    elif self.q_number != 100:
                        self.payoff3 = 0
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                elif self.treatment == "ButtonB":  # treatment B and press
                    if self.q_number == 100:
                        self.payoff3 = 0.1
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                    elif self.q_number != 100:
                        self.payoff3 = 0
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
            else:
                if self.treatment == "ButtonA": # treatment A and not press
                    if self.q_number == 100:
                        self.payoff3 = 0.1
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                    elif self.q_number != 100:
                        self.payoff3 = 0
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                elif self.treatment == "ButtonB":  # treatment B and  not press
                    if self.q_number == 100:
                        self.payoff3 = 0.1
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                    elif self.q_number != 100:
                        self.payoff3 = 0
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])

    def set_payoffsdanat(self):
        if self.treatment == "NoButton":
            if self.selected ==1:
                if self.secondary_button == "A":
                    if self.q_number == 100:
                        self.payoff3 = 10.1
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                    elif self.q_number != 100:
                        self.payoff3 = 10
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                if self.secondary_button == "B":
                    if self.q_number == 100:
                        self.payoff3 = 3.1
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                    elif self.q_number != 100:
                        self.payoff3 = 3
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
            elif self.selected == 0:
                if self.secondary_button == "A":
                    if self.q_number == 100:
                        self.payoff3 = 0.1
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                    elif self.q_number != 100:
                        self.payoff3 = 0
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                if self.secondary_button == "B":
                    if self.q_number == 100:
                        self.payoff3 = 0.1
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                    elif self.q_number != 100:
                        self.payoff3 = 0
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
        else:
            pass



