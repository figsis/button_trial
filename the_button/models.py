
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
    optionA = [5, 15]  # bonus payments NO CLICK [receiver, charity]
    optionB = [10, 0]  # bonus payment CLICK
    optionA0=optionA[0]
    optionA1=optionA[1]
    optionB0=optionB[0]
    optionB1=optionB[1]
    timer = 30 # in seconds
    dana2A_self = 10
    dana2A_other = 0
    dana2B_self = 5
    dana2B_other = 15
    numberList = [1, 0]

class Subsession(BaseSubsession):
    def creating_session(self):
        for player in self.get_players():
            player.treatment = random.choice(["ButtonA", "ButtonB","NoButton"])
            self.session.vars["treatment"] = player.treatment
            player.selected= random.choices(Constants.numberList, weights=(50,50), k=1)[0] #10,90
            self.session.vars["selected"] = player.selected
            #player.participant.vars["payoff2_self"] = ""
            player.participant.vars["payoff3"] = ""
            #player.participant.vars["payoff2_charity"] = ""
            player.participant.vars["payoff2_self_danat"] = ""
            player.participant.vars["payoff2_charity_danat"] = ""
            player.participant.vars["bonus"] = ""
            #player.participant.vars["danat"] = ""
        #    player.participant.vars["too_long"] = False



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    prolific_id = models.StringField()
    treatment = models.StringField()
    button = models.BooleanField(initial=0)
    bonus = models.FloatField()
    store_time = models.FloatField()  # for the timer
    store_timeA = models.FloatField()
    store_timeB = models.FloatField()
    payoff2_self = models.IntegerField()  # payoff task 2 (button)
    # payoff2 = models.IntegerField()
    payoff3 = models.FloatField()

    payoff4 = models.FloatField()
    #payoff2o = models.IntegerField()
    payoff2_charity = models.IntegerField()  # payoff task 2 (button)
    danat = models.StringField(blank=True)  # whether participant takes selfish choice in Dana timed task
    secondaryButton= models.IntegerField()
    payoff2_self_danat = models.IntegerField()  # payoff dana_timed
    payoff2_charity_danat = models.IntegerField()  # payoff dana_timed
    #total_payoff = models.FloatField()
    # How strong was the temptation to press the button?
    q0 = models.IntegerField(label='How strong was the temptation to press the button? 0: not tempting at al. 10: very tempting. ', choices=[0,1, 2, 3, 4, 5, 6, 7, 8, 9,10],
        widget=widgets.RadioSelectHorizontal)
    #Reasons to press
    q1 = models.LongStringField(label='Why did you decide to press the button?')
    q2 = models.LongStringField(label='Why did you decide not to press the button?')
    #Why did you change/did not change your final decision? In all treatments every time a discrepancy between decisions.
    q_change = models.LongStringField(label='Why did you change your mind?')
    q_nochange = models.LongStringField(label='Why did you not change your mind?' )
    #What was the highest number that you saw appear on screen?
    q_number = models.IntegerField(label="What was the highest number that you saw appearing on screen?", min=0, max=10000)
    selected = models.IntegerField()
    q_feedback = models.LongStringField(label="This is the end of the survey. "
                                            "In case you have comments, please leave them here.",
                                      blank=True)
    q_feedback_pilot = models.LongStringField(label="If you found any instructions unclear or confusing, please let us know here.",
                                            blank=True)



    def set_payoffs(self):
            if self.treatment == "ButtonA":
                if self.store_time != 0:
                    self.payoff2_self=Constants.optionB[0]
                    self.payoff2_charity = Constants.optionB[1]
                elif self.store_time == 0:
                    self.payoff2_self = Constants.optionA[0]
                    self.payoff2_charity = Constants.optionA[1]
            elif self.treatment == "ButtonB":
                if self.store_time != 0:
                    self.payoff2_self = Constants.optionA[0]
                    self.payoff2_charity = Constants.optionA[1]
                else: #not pressing the button yields the selfish action
                    self.payoff2_self = Constants.optionA[0]
                    self.payoff2_charity = Constants.optionA[1]
            elif self.session.vars["treatment"] == "NoButton":
                if self.danat == "A":
                    self.payoff2_self_danat = Constants.dana2A_self
                    self.payoff2_charity_danat = Constants.dana2A_other
                elif self.danat == "B":
                    self.payoff2_self_danat = Constants.dana2B_self
                    self.payoff2_charity_danat = Constants.dana2B_other


    def set_bonus(self):
        if self.q_number == 100:
            self.participant.vars["bonus"] = 0.5
            self.bonus = self.participant.vars["bonus"]
        elif self.q_number != 100:
            self.bonus = 0


    def set_payoff3(self):
        if self.selected == 1:
            if self.store_time != 0:
                if self.treatment == "ButtonA":  #treatment A and press
                    if self.q_number == 100:
                        self.payoff3 = 10.5
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                    elif self.q_number != 100:
                        self.payoff3 = 10
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                elif self.treatment == "ButtonB":  # treatment B and press
                    if self.q_number == 100:
                        self.payoff3 = 5.5
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                    elif  self.q_number != 100:
                        self.payoff3=5
                        self.payoff4 = self.payoff3+ float(self.participant.vars["payoff_svo"])
            else: #button not pressed
                if self.treatment == "ButtonA": #treatment A and not press
                    if self.q_number == 100:
                        self.payoff3 = 5.5
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                    elif self.q_number != 100:
                        self.payoff3 = 5
                        self.payoff4 = self.payoff3+ float(self.participant.vars["payoff_svo"])
                elif self.treatment == "ButtonB":  # treatment B and  not press
                    if self.q_number == 100:
                        self.payoff3 = 10.5
                        self.payoff4  = self.payoff3+ float(self.participant.vars["payoff_svo"])
                    elif self.q_number != 100:
                        self.payoff3 = 10
                        self.payoff4 = self.payoff3+float(self.participant.vars["payoff_svo"])
        elif self.selected == 0:
            if self.store_time != 0:
                if self.treatment == "ButtonA": # treatment A and press
                    if self.q_number == 100:
                        self.payoff3 = 0.5
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                    elif self.q_number != 100:
                        self.payoff3 = 0
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                elif self.treatment == "ButtonB":  # treatment B and press
                    if self.q_number == 100:
                        self.payoff3 = 0.5
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                    elif self.q_number != 100:
                        self.payoff3 = 0
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
            else:
                if self.treatment == "ButtonA": # treatment A and not press
                    if self.q_number == 100:
                        self.payoff3 = 0.5
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                    elif self.q_number != 100:
                        self.payoff3 = 0
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                elif self.treatment == "ButtonB":  # treatment B and  not press
                    if self.q_number == 100:
                        self.payoff3 = 0.5
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                    elif self.q_number != 100:
                        self.payoff3 = 0
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])

    def set_payoffsdanat(self):
        if self.treatment == "NoButton":
            if self.selected ==1:
                if self.danat == "A":
                    if self.q_number == 100:
                        self.payoff3 =10.5
                        self.payoff4  = self.payoff3 + float(self.participant.vars["payoff_svo"])
                    elif self.q_number !=100 :
                        self.payoff3 = 10
                        self.payoff4  = self.payoff3 + float(self.participant.vars["payoff_svo"])
                if self.danat == "B":
                    if self.q_number == 100:
                        self.payoff3 =5.5
                        self.payoff4  = self.payoff3 + float(self.participant.vars["payoff_svo"])
                    elif self.q_number !=100 :
                        self.payoff3 = 5
                        self.payoff4  = self.payoff3 + float(self.participant.vars["payoff_svo"])
            elif self.selected == 0:
                if self.danat == "A":
                    if self.q_number == 100:
                        self.payoff3 = 0.5
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                    elif self.q_number != 100:
                        self.payoff3 = 0
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                if self.danat == "B":
                    if self.q_number == 100:
                        self.payoff3 = 0.5
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
                    elif self.q_number != 100:
                        self.payoff3 = 0
                        self.payoff4 = self.payoff3 + float(self.participant.vars["payoff_svo"])
        else:
            pass



