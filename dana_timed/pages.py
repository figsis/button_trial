from ._builtin import Page
from .models import Constants
from .stuff import UnderstandingQuestionsPage
import random


class SummaryTask1_(Page):
    form_model = 'player'



class task_timed(Page):
        form_model = 'player'
        form_fields = ['danat', 'store_time']
        timeout_seconds = Constants.timer

        def before_next_page(self):
            self.player.set_payoffs2()



#class Results(Page):
#    form_model = 'player'

#    def vars_for_template(self):
#        return dict(
#                    payoff2_self_danat=self.player.payoff1_self_danat,
#                    payoff1_charity_danat=self.player.payoff1_charity_danat,
#                    )

class Survey(Page):
    form_model = 'player'
    form_fields = ['q1', 'q_diff']



    #def before_next_page(self):
     #   import time
        # start timer to find out how long a person is stuck on next wait page
        #  self.player.participant.vars["wait_page_arrival"] = time.time()
        # self.player.participant.vars["too_long"] = False

page_sequence = [


    #InstructionsTask1,
    SummaryTask1_,
    task_timed,
    Survey,
    #SummaryTask1
]
