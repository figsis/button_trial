from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)





doc = """
     
      """

# Config for the game
class Constants(BaseConstants):
    name_in_url = 'dat'
    players_per_group = None         # The number should be a multiple of 2 in case the matching is RANDOM_DICTATOR.
    num_rounds = 1
    participation_fee = 0.75  # in pounds
    prolific_id = models.StringField()


# Defining what configs to be saved
class Subsession(BaseSubsession):
  pass

class Group(BaseGroup):
    pass



# Player base class which contains the values for a single player per game
class Player(BasePlayer):
    prolific_id = models.StringField()
    word1= models.StringField()
    word2= models.StringField()
    word3= models.StringField()
    word4= models.StringField()
    word5= models.StringField()
    word6= models.StringField()
    word7= models.StringField() #https://www.datcreativity.com/analyse
    word8 = models.StringField()
    word9 = models.StringField()
    word10 = models.StringField()


