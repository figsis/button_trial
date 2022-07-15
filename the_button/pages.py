# from project._builtin import Page, WaitPage
from ._builtin import Page, WaitPage
from .models import Constants
from otree.api import *
from .models import Player


def vars_for_all_templates(self):
    return {
        'treatment': self.participant.vars["treatment"],
        'selected':  self.session.vars["selected"]}


class SummaryTask1_(Page):
    def is_displayed(self):
        player = self.player
        return player.treatment == "ButtonA" or player.treatment == "ButtonB"


class SummaryTask1_danat(Page):
    def is_displayed(self):
        player = self.player
        return player.treatment == "NoButton"

class Instructions_Attention(Page):
    pass

class Button(Page):
    form_model = 'player'
    form_fields = ['button', 'store_time']
    timeout_seconds = Constants.timer

    def is_displayed(self):
        player = self.player
        return player.treatment == "ButtonA" or player.treatment == "ButtonB"

#class ButtonClicked(Page):
    #   form_model = 'player'

        #  def get_timeout_seconds(self):
    #      return self.player.store_time

        #  def is_displayed(self):
        #      player = self.player
#      return player.treatment == "ButtonA" and player.button==1 or player.treatment == "ButtonB" and player.button==1


#class danat_clicked(Page):
    #   form_model = 'player'
    #form_fields = ['danat']

    #def get_timeout_seconds(self):
    #   return self.player.store_time

    ##def is_displayed(self):
        #  player = self.player
        #return player.treatment == "NoButton"







class task_timed(Page):
    form_model = 'player'
    form_fields = ['danat','secondary_button', 'store_time', 'store_timeB'] #'store_time'
    timeout_seconds = Constants.timer

    def is_displayed(self):
        player = self.player
        return player.treatment == "NoButton"

class Error(Page):
    form_model = 'player'
    form_fields = [ 'store_time', 'store_timeB',"secondary_button"]  # 'store_time'

    def is_displayed(self):
        player = self.player
        return player.treatment == "NoButton" and player.secondary_button == ""

    def error_message(self, values):
        if self.player.secondary_button == "":
            return 'Error. You did not select any option. Please select an option'


class Payment(Page):
    form_model = 'player'
    form_fields = [ 'bonus', 'payoff2_self', 'payoff2_charity', 'payoff2_self_danat',
                    'payoff2_charity_danat', 'payoff3', 'treatment']
    def vars_for_template(self):
        return dict(
            payoff_svo=self.player.participant.vars["payoff_svo"],
            payoff_svo_other=self.player.participant.vars["payoff_svo_other"],
            #payoff2_charity=self.player.participant.vars["payoff2_charity"],
            payoff2_charity=self.player.payoff2_charity,
            payoff2_charity_danat=self.player.payoff2_charity_danat,
            #paid_slider = self.player.participant.vars["paid_slider"],
            selected=self.player.selected,
            payoff2_self=self.player.payoff2_self,
            payoff2_self_danat=self.player.payoff2_self_danat,
            bonus= self.player.bonus,
            payoff3= self.player.payoff3,
            payoff4 = self.player.payoff4,
            treatment = self.player.treatment,

        )
    def js_vars(self):
        cc_code = self.session.config["cc_code"]
        link = "https://app.prolific.co/submissions/complete?cc=" + str(cc_code)
        return dict(
            completionlink=link
        )
    pass

class Attention_Survey(Page):
    form_model = 'player'
    form_fields = ['q_number']

    def vars_for_template(self):
        return dict(q_number=self.player.q_number)
    def before_next_page(self):
        self.player.set_payoffs()



class Survey(Page):
    form_model = 'player'
    form_fields = []

    def vars_for_template(self):
        return dict(payoff1_self=self.player.participant.vars["payoff1_self"],
                    payoff2_self=self.player.payoff2_self,
                    store_time = self.player.store_time)

    def is_displayed(self):
        player = self.player
        return player.treatment == "ButtonA" or player.treatment == "ButtonB"

    def get_form_fields(self):
        if self.player.treatment == "ButtonA":
            #selfish button pressed but altruistic dana (altruistic-selfish)
            if self.player.store_time != 0 and self.participant.vars["payoff1_self"]  == 5:
                return ['q0', 'q1','q_change']
            #selfish button pressed and selfish dana (selfish-selfish)
            elif self.player.store_time != 0 and self.participant.vars["payoff1_self"]  ==10:
                return ['q0','q1','q_nochange']
            # selfish button not pressed and selfish dana (selfish-altruistic)
            elif self.player.store_time == 0 and self.participant.vars["payoff1_self"]  ==10:
                return ['q0','q2','q_change']
            # selfish button not pressed and altruistic dana (altruistic-altruistic)
            elif self.player.store_time == 0 and self.participant.vars["payoff1_self"] == 5:
                return ['q0','q2','q_nochange']
        if self.player.treatment == "ButtonB":
            #altruistic button pressed and altruistic dana (altruistic-altruistic)
            if self.player.store_time != 0 and self.participant.vars["payoff1_self"]  == 5:
                return ['q0', 'q1',  'q_nochange']
            #altruistic button pressed and selfish dana (selfish-altruistic)
            elif self.player.store_time != 0 and self.participant.vars["payoff1_self"]  ==10:
                return ['q0', 'q1', 'q_change']
            #altruistic button not pressed and selfish dana (selfish-selfish)
            elif self.player.store_time == 0 and self.participant.vars["payoff1_self"]  ==10:
                return ['q0', 'q2',  'q_nochange']
            # altruistic button not pressed and altruistic dana (altruistic-selfish)
            elif self.player.store_time == 0 and self.participant.vars["payoff1_self"] == 5:
                return ['q0', 'q2',  'q_change']

    def before_next_page(self):
        self.player.set_payoffs()
        self.player.set_bonus()
        self.player.set_payoff3()


class Survey_danat(Page):
    form_model = 'player'
    form_fields = []

    def vars_for_template(self):
        return dict(task1=self.player.participant.vars["task1"],
                    secondary_button= self.player.secondary_button)

    def get_form_fields(self):
        if self.participant.vars["task1"] == self.player.secondary_button:
            return ['q_nochange']
        elif self.participant.vars["task1"] == self.player.secondary_button:
            return ['q_change']


    def is_displayed(self):
        player = self.player
        return player.treatment == "NoButton"

    def before_next_page(self):
        self.player.set_bonus()
        self.player.set_payoffsdanat()


class Comments(Page):
    form_model = 'player'
    form_fields = ['q_feedback', 'q_feedback_pilot']



page_sequence = [SummaryTask1_,
                 SummaryTask1_danat,
                 Instructions_Attention,
                 Button,
                 #ButtonClicked,
                 task_timed,
                 Error,
                 #danat_clicked,
                 Attention_Survey,
                 Survey,
                 Survey_danat,
                 Comments,
                 Payment
                 ]
