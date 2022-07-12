
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
            player.participant.vars["total_payoff"] = ""
            player.participant.vars["payoff2_self"] = ""
            player.participant.vars["payoff2"] = ""
            player.participant.vars["payoff3"] = ""
            player.participant.vars["payoff2o"] = ""
            player.participant.vars["payoff2_charity"] = ""
            player.participant.vars["payoff2_self_danat"] = ""
            player.participant.vars["payoff2_charity_danat"] = ""
            player.participant.vars["bonus"] = ""
            player.participant.vars["danat"] = ""
        #    player.participant.vars["too_long"] = False



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    prolific_id = models.StringField()
    treatment = models.StringField()
    button = models.BooleanField(initial=0)
    bonus = models.FloatField()
    store_time = models.FloatField()  # for the timer
    payoff2_self = models.IntegerField()  # payoff task 2 (button)
    # payoff2 = models.IntegerField()
    payoff3 = models.IntegerField()
    #payoff2o = models.IntegerField()
    payoff2_charity = models.IntegerField()  # payoff task 2 (button)
    danat = models.StringField(blank=False)  # whether participant takes selfish choice in Dana timed task
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
            #bonus contingent on treatments
            if self.treatment == "ButtonA":
                #if self.button==1: #presing yields selfish option b
                #if self.session.vars["selected"] == 1:
                if self.store_time != 0:
                    self.participant.vars["payoff2_self"] = Constants.optionB[0] #10
                    self.participant.vars["payoff2_charity"] = Constants.optionB[1] #0
                    self.payoff2_self = self.participant.vars["payoff2_self"]  # to store to the oTree database
                    self.payoff2_charity = self.participant.vars["payoff2_charity"]
                 #       self.payoff2 = self.participant.vars["payoff2_self"]
                  #      self.payoff2o = self.participant.vars["payoff2_charity"]
                elif self.store_time == 0:
                    self.participant.vars["payoff2_self"] = Constants.optionA[0] #5
                    self.participant.vars["payoff2_charity"] = Constants.optionA[1] #15
                    self.payoff2_self = self.participant.vars["payoff2_self"]  # to store to the oTree database
                    self.payoff2_charity = self.participant.vars["payoff2_charity"]
            elif self.treatment == "ButtonB":
                #if self.button==1: #pressing the button yields the prosocial action
                if self.store_time != 0:
                    self.participant.vars["payoff2_self"] = Constants.optionA[0]  #5
                    self.participant.vars["payoff2_charity"] = Constants.optionA[1] #15
                else: #not pressing the button yields the selfish action
                    self.participant.vars["payoff2_self"] = Constants.optionB[0] #10
                    self.participant.vars["payoff2_charity"] = Constants.optionB[1] #0
                self.payoff2_self = self.participant.vars["payoff2_self"]  # to store to the oTree database
                self.payoff2_charity = self.participant.vars["payoff2_charity"]
            elif self.session.vars["treatment"] == "NoButton":
                if self.danat == "A":
                    self.player.participant.vars["danat"] == "A"
                    self.participant.vars["payoff2_self_danat"] = Constants.dana2A_self
                    self.participant.vars["payoff2_charity_danat"] = Constants.dana2A_other
                elif self.danat == "B":
                    self.player.participant.vars["danat"] == "B"
                    self.participant.vars["payoff2_self_danat"] = Constants.dana2B_self # 10
                    self.participant.vars["payoff2_charity_danat"] = Constants.dana2B_other# 10
            # to store for next app (button task + final payoffs)
                self.payoff2_self_danat = self.participant.vars["payoff2_self_danat"]  # to store to the oTree database
                self.payoff2_charity_danat = self.participant.vars["payoff2_charity_danat"]
                self.danat=self.player.participant.vars["danat"]
               # if self.session.vars["selected"] == 1:
                #    self.payoff2 = self.participant.vars["payoff2_self_danat"]
                 #   self.participant.vars["payoff2"] = self.payoff2
                 ##   self.payoff2o = self.participant.vars["payoff2_charity_danat"]
                   # self.participant.vars["payoff2o"] = self.payoff2o
                #else:
                 #   self.payoff2 = 0
                  #  self.payoff2o = 0

    def set_bonus(self):
        if self.q_number == 100:
            self.participant.vars["bonus"] = 0.5
            self.bonus = self.participant.vars["bonus"]
        elif self.q_number != 100:
            self.bonus = 0

        # def total_payoff(self):
        #if self.selected == 1:
            #   self.total_payoff = cu(self.participant.vars["bonus"] + self.payoff2_self)
            #self.participant.vars["total_payoff"] = self.total_payoff
            # + self.participant.vars["payoff_svo"])
            #self.total_payoff = self.participant.vars["total_payoff"]
            #elif self.selected == 0:
            #self.total_payoff = cu(self.participant.vars["bonus"]) # + self.participant.vars["payoff_svo"])
            #self.participant.vars["total_payoff"] = self.total_payoff

    def set_payoff3(self):
        if self.selected == 1:
            if self.treatment=="ButtonA":
                if self.store_time !=0 :
                    if self.q_number == 100:
                        self.payoff3 = 10.5
                        self.participant.vars["payoff3"] = self.payoff3 +float(self.participant.vars["payoff_svo"])
                        self.payoff3 = self.participant.vars["payoff3"]
                    else:
                        self.payoff3=10
                        self.participant.vars["payoff3"] = self.payoff3 + float(self.participant.vars["payoff_svo"])
                        self.payoff3 = self.participant.vars["payoff3"]
                else:
                    if self.q_number == 100:
                        self.payoff3 = 5.5
                        self.participant.vars["payoff3"] = self.payoff3+float(self.participant.vars["payoff_svo"])
                        self.payoff3 = self.participant.vars["payoff3"]
                    else:
                        self.payoff3=5
                        self.participant.vars["payoff3"] = self.payoff3+float(self.participant.vars["payoff_svo"])
                        self.payoff3 = self.participant.vars["payoff3"]
            elif self.treatment == "ButtonB":
                if self.store_time!=0:
                    if self.q_number == 100:
                        self.payoff3 = 5.5
                        self.participant.vars["payoff3"] = self.payoff3+ float(self.participant.vars["payoff_svo"])
                        self.payoff3 = self.participant.vars["payoff3"]
                    else:
                        self.payoff3=5
                        self.participant.vars["payoff3"] = self.payoff3+ float(self.participant.vars["payoff_svo"])
                        self.payoff3 = self.participant.vars["payoff3"]
                else:
                    if self.q_number == 100:
                        self.payoff3 = 10.5
                        self.participant.vars["payoff3"] = self.payoff3+ float(self.participant.vars["payoff_svo"])
                        self.payoff3 = self.participant.vars["payoff3"]
                    else:
                        self.payoff3 = 10
                        self.participant.vars["payoff3"] = self.payoff3+float(self.participant.vars["payoff_svo"])
                        self.payoff3 = self.participant.vars["payoff3"]
            elif self.treatment == "NoButton":
                if self.q_number == 100:
                    if self.danat == "A":
                        self.payoff3 =10.5
                        self.participant.vars["payoff3"] = self.payoff3 + float(self.participant.vars["payoff_svo"])
                        self.payoff3 = self.participant.vars["payoff3"]
                    if self.danat == "B":
                        self.payoff3 = 5.5
                        self.participant.vars["payoff3"] = self.payoff3 + float(self.participant.vars["payoff_svo"])
                        self.payoff3 = self.participant.vars["payoff3"]
                else:
                    if self.danat == "A":
                        self.payoff3 =0.5
                        self.participant.vars["payoff3"] = self.payoff3 + float(self.participant.vars["payoff_svo"])
                        self.payoff3 = self.participant.vars["payoff3"]
                    if self.danat == "B":
                        self.payoff3 = 0.5
                        self.participant.vars["payoff3"] = self.payoff3 + float(self.participant.vars["payoff_svo"])
                        self.payoff3 = self.participant.vars["payoff3"]
        elif self.selected == 0:
            if self.treatment=="ButtonA":
                if self.store_time !=0 :
                    if self.q_number == 100:
                        self.payoff3 = 0.5
                        self.participant.vars["payoff3"] = self.payoff3+float(self.participant.vars["payoff_svo"])
                        self.payoff3 = self.participant.vars["payoff3"]
                    else:
                        self.payoff3=0
                        self.participant.vars["payoff3"] = self.payoff3 + float(self.participant.vars["payoff_svo"])
                        self.payoff3 = self.participant.vars["payoff3"]
                else:
                    if self.q_number == 100:
                        self.payoff3 = 0.5
                        self.participant.vars["payoff3"] = self.payoff3 + float(self.participant.vars["payoff_svo"])
                        self.payoff3 = self.participant.vars["payoff3"]
                    else:
                        self.payoff3=0
                        self.participant.vars["payoff3"] = self.payoff3 + float(self.participant.vars["payoff_svo"])
                        self.payoff3 = self.participant.vars["payoff3"]
            elif self.treatment == "ButtonB":
                if self.store_time!=0:
                    if self.q_number == 100:
                        self.payoff3 = 0.5
                        self.participant.vars["payoff3"] = self.payoff3+ float(self.participant.vars["payoff_svo"])
                        self.payoff3 = self.participant.vars["payoff3"]
                    else:
                        self.payoff3=0
                        self.participant.vars["payoff3"] = self.payoff3+ float(self.participant.vars["payoff_svo"])
                        self.payoff3 = self.participant.vars["payoff3"]
                else:
                    if self.q_number == 100:
                        self.payoff3 = 0.5
                        self.participant.vars["payoff3"] = self.payoff3+ float(self.participant.vars["payoff_svo"])
                        self.payoff3 = self.participant.vars["payoff3"]
                    else:
                        self.payoff3=0
                        self.participant.vars["payoff3"] = self.payoff3+ float(self.participant.vars["payoff_svo"])
                        self.payoff3 = self.participant.vars["payoff3"]
            elif self.treatment == "NoButton":
                if self.q_number == 100:
                    if self.danat == "A":
                        self.payoff3 = 0.5
                        self.participant.vars["payoff3"] = self.payoff3 + float(self.participant.vars["payoff_svo"])
                        self.payoff3 = self.participant.vars["payoff3"]
                    if self.danat == "B":
                        self.payoff3 = 0.5
                        self.participant.vars["payoff3"] = self.payoff3 + float(self.participant.vars["payoff_svo"])
                        self.payoff3 = self.participant.vars["payoff3"]
                else:
                    if self.danat == "A":
                        self.payoff3 = 0
                        self.participant.vars["payoff3"] = self.payoff3 + float(self.participant.vars["payoff_svo"])
                        self.payoff3 = self.participant.vars["payoff3"]
                    if self.danat == "B":
                        self.payoff3 = 0
                        self.participant.vars["payoff3"] = self.payoff3 + float(self.participant.vars["payoff_svo"])
                        self.payoff3 = self.participant.vars["payoff3"]





