from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class Welcome(Page):
    form_model = 'player'


class GeneralInstructions(Page):
    form_model = 'player'
    form_fields = ['prolific_id']

    def before_next_page(self):
        #self.player.browser = self.request.META.get('HTTP_USER_AGENT')
        self.player.participant.vars["prolific_id"] = self.player.prolific_id
        self.player.participant.vars["participation_fee"] = Constants.participation_fee


class Words(Page):
	form_model = 'player'
	form_fields = [
		'word1','word2',
		'word3','word4',
		'word5','word6',
		'word7', 'word8',
		'word9', 'word10']


page_sequence = [
	Welcome,
	GeneralInstructions,
	Words,
]
