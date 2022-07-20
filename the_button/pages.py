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
        return player.treatment == "ButtonA"

class Button2(Page):
    form_model = 'player'
    form_fields = ['button', 'store_time']
    timeout_seconds = Constants.timer

    def is_displayed(self):
        player = self.player
        return player.treatment == "ButtonB"

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
    form_fields = ['danat','secondary_button', 'store_timeA', 'store_timeB'] #'store_time'
    timeout_seconds = Constants.timer

    def is_displayed(self):
        player = self.player
        return player.treatment == "NoButton"

class Error(Page):
    form_model = 'player'
    form_fields = ['store_time', 'store_timeB',"secondary_button"]  # 'store_time'

    def is_displayed(self):
        player = self.player
        return player.treatment == "NoButton" and player.secondary_button == ""

    def error_message(self, values):
        if self.player.secondary_button == "":
            return 'Error. You did not select any option. Please select an option'

    def js_vars(self):
        error_code = self.session.config["error_code"]
        link = "https://app.prolific.co/submissions/complete?cc=" + str(error_code)
        return dict(
            errorlink=link
        )
    pass

class Attention_Survey(Page):
    form_model = 'player'
    form_fields = ['q_number']

    def vars_for_template(self):
        return dict(q_number=self.player.q_number)

    def before_next_page(self):
        self.player.set_payoffs()

class Survey1(Page):
    form_model = 'player'
    form_fields =  ['q0', 'q1', 'q_change']

    def is_displayed(self):
        player = self.player
        return player.treatment == "ButtonA" and self.player.store_time != 0 and self.participant.vars["payoff1_self"] == 3

    def before_next_page(self):
        self.player.set_bonus()
        self.player.set_payoff3()



class Survey2(Page):
    form_model = 'player'
    form_fields = ['q0','q1','q_nochange']

    def is_displayed(self):
        player = self.player
        return player.treatment == "ButtonA" and self.player.store_time != 0 and self.participant.vars["payoff1_self"] == 10

    def before_next_page(self):
        self.player.set_bonus()
        self.player.set_payoff3()


class Survey3(Page):
    form_model = 'player'
    form_fields = ['q0','q2','q_change']
    def is_displayed(self):
        player = self.player
        return player.treatment == "ButtonA" and self.player.store_time == 0 and self.participant.vars["payoff1_self"] == 10
    def before_next_page(self):
        self.player.set_bonus()
        self.player.set_payoff3()


class Survey4(Page):
    form_model = 'player'
    form_fields = ['q0','q2','q_nochange']

    def is_displayed(self):
        player = self.player
        return player.treatment == "ButtonA" and self.player.store_time == 0 and self.participant.vars[
            "payoff1_self"] == 3
    def before_next_page(self):
        self.player.set_bonus()
        self.player.set_payoff3()


class Survey5(Page):
    form_model = 'player'
    form_fields = ['q0', 'q1',  'q_nochange']

    def is_displayed(self):
        player = self.player
        return player.treatment == "ButtonB" and self.player.store_time != 0 and self.participant.vars["payoff1_self"] == 3

    def before_next_page(self):
        self.player.set_bonus()
        self.player.set_payoff3()


class Survey6(Page):
    form_model = 'player'
    form_fields = ['q0', 'q1', 'q_change']

    def is_displayed(self):
        player = self.player
        return player.treatment == "ButtonB" and self.player.store_time != 0 and self.participant.vars["payoff1_self"] == 10

    def before_next_page(self):
        self.player.set_bonus()
        self.player.set_payoff3()


class Survey7(Page):
    form_model = 'player'
    form_fields = ['q0', 'q2',  'q_nochange']

    def is_displayed(self):
        player = self.player
        return player.treatment == "ButtonB" and self.player.store_time == 0 and self.participant.vars["payoff1_self"] == 10
    def before_next_page(self):
        self.player.set_bonus()
        self.player.set_payoff3()


class Survey8(Page):
    form_model = 'player'
    form_fields = ['q0', 'q2',  'q_change']

    def is_displayed(self):
        player = self.player
        return player.treatment == "ButtonB" and self.player.store_time == 0 and self.participant.vars["payoff1_self"] == 3

    def before_next_page(self):
        self.player.set_bonus()
        self.player.set_payoff3()


class Survey(Page):
    form_model = 'player'
    form_fields = []

    def is_displayed(self):
        player = self.player
        return player.treatment == "ButtonA" or player.treatment == "ButtonB"

    def get_form_fields(self):
        if self.player.treatment == "ButtonA":
           #selfish button pressed but altruistic dana (altruistic-selfish)
            if self.player.store_time != 0 and self.participant.vars["payoff1_self"]  == 3:
                return ['q0', 'q1','q_change']
           # selfish button pressed and selfish dana (selfish-selfish)
            elif self.player.store_time != 0 and self.participant.vars["payoff1_self"]  ==10:
                return ['q0','q1','q_nochange']
             #selfish button not pressed and selfish dana (selfish-altruistic)
            elif self.player.store_time == 0 and self.participant.vars["payoff1_self"]  ==10:
                return ['q0','q2','q_change']
            # selfish button not pressed and altruistic dana (altruistic-altruistic)
            elif self.player.store_time == 0 and self.participant.vars["payoff1_self"] == 3:
                return ['q0','q2','q_nochange']
        elif self.player.treatment == "ButtonB":
          #  altruistic button pressed and altruistic dana (altruistic-altruistic)
            if self.player.store_time != 0 and self.participant.vars["payoff1_self"]  == 3:
               return ['q0', 'q1',  'q_nochange']
            #altruistic button pressed and selfish dana (selfish-altruistic)
            elif self.player.store_time != 0 and self.participant.vars["payoff1_self"]  ==10:
               return ['q0', 'q1', 'q_change']
            #altruistic button not pressed and selfish dana (selfish-selfish)
            elif self.player.store_time == 0 and self.participant.vars["payoff1_self"]  ==10:
               return ['q0', 'q2',  'q_nochange']
            # altruistic button not pressed and altruistic dana (altruistic-selfish)
            elif self.player.store_time == 0 and self.participant.vars["payoff1_self"] == 3:
               return ['q0', 'q2',  'q_change']
        else:
            return []

    def before_next_page(self):
        self.player.set_bonus()
        self.player.set_payoff3()


class Survey_danat(Page):
    form_model = 'player'
    form_fields =['q_nochange']

   # def get_form_fields(self):
    #    if self.participant.vars["treatment"] == "NoButton":
    #       if self.participant.vars["task1"] == self.player.secondary_button:
    #           return ['q_nochange']
    #       elif self.participant.vars["task1"] == self.player.secondary_button:
    #           return ['q_change']
    #   else:
    #       pass


    def is_displayed(self):
        player = self.player
        return player.treatment == "NoButton" and self.participant.vars["task1"] == self.player.secondary_button

    def before_next_page(self):
        self.player.set_bonus()
        self.player.set_payoffsdanat()


class Survey_danatC(Page):
    form_model = 'player'
    form_fields = ['q_change']

    def is_displayed(self):
        return self.player.treatment == "NoButton" and self.participant.vars["task1"] != self.player.secondary_button

    def before_next_page(self):
        self.player.set_bonus()
        self.player.set_payoff3()
        self.player.set_payoffsdanat()


class Comments(Page):
    form_model = 'player'
    form_fields = ['q_feedback', 'q_feedback_pilot']


class Payment(Page):
    form_model = 'player'
    form_fields = ['bonus', 'payoff2_self', 'payoff2_charity', 'payoff2_self_danat',
                   'payoff2_charity_danat', 'payoff3', 'treatment']

    def vars_for_template(self):
        return dict(
            payoff_svo=self.player.participant.vars["payoff_svo"],
            payoff_svo_other=self.player.participant.vars["payoff_svo_other"],
            payoff2_charity=self.player.payoff2_charity,
            payoff2_charity_danat=self.player.payoff2_charity_danat,
            # paid_slider = self.player.participant.vars["paid_slider"],
            selected=self.player.selected,
            payoff2_self=self.player.payoff2_self,
            payoff2_self_danat=self.player.payoff2_self_danat,
            bonus=self.player.bonus,
            payoff3=self.player.payoff3,
            payoff4=self.player.payoff4,
            treatment=self.player.treatment
        )

    def js_vars(self):
        cc_code = self.session.config["cc_code"]
        link = "https://app.prolific.co/submissions/complete?cc=" + str(cc_code)
        return dict(
            completionlink=link
        )

    pass


page_sequence = [
                 SummaryTask1_,
                 SummaryTask1_danat,
                 Instructions_Attention,
                 Button,
                 Button2,
                 task_timed,
                 Error,
                 Attention_Survey,
                 Survey1,
                 Survey2,
                 Survey3,
                 Survey4,
                 Survey5,
                 Survey6,
                 Survey7,
                 Survey8,
                 Survey_danat,
                 Survey_danatC,
                 Comments,
                 Payment
                 ]
