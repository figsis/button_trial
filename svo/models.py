from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random
from math import atan, degrees, sqrt, tan, pi

from otree.models import player

from .utils import compute_line, intersection_point, distance, max_tuple

author = 'Abdul Majeed Alkattan, Emad Bahrami'

doc = """
      Social Value Orientation
      """


# Config for the game
class Constants(BaseConstants):
    name_in_url = 'svo'
    players_per_group = None  # The number should be a multiple of 2 in case the matching is RANDOM_DICTATOR.
    num_rounds = 1

    slider_end_points = {
        'item7': [(100, 50), (70, 100)],
        'item8': [(90, 100), (100, 90)],
        'item9': [(100, 70), (50, 100)],
        'item10': [(100, 70), (90, 100)],
        'item11': [(70, 100), (100, 70)],
        'item12': [(50, 100), (100, 90)],
        'item13': [(50, 100), (100, 50)],
        'item14': [(100, 90), (70, 100)],
        'item15': [(90, 100), (100, 50)]}

    # representing line y=x using Ax+By=C by A, B, C
    identity_line = (1, -1, 0)

    line = compute_line
    id_line = identity_line
    # intersection point of the slider line and y=x line
    mid_points = {}
    # store th joint max of each item
    joint_max = {}
    # points that always maximize other
    altruist_points = {}
    # points that always maximize self
    individualist_points = {}
    secondary_items = []
    for item, points in slider_end_points.items():
        mid_points[item] = intersection_point(id_line, line(*points))
        joint_max[item] = max_tuple(*points, sum)
        altruist_points[item] = max_tuple(*points, lambda x: x[1])
        individualist_points[item] = max_tuple(*points, lambda x: x[0])
        secondary_items.append(item)


# Defining what configs to be saved
class Subsession(BaseSubsession):
    select_items = models.StringField(choices=['PRIMARY', 'FULL'])
    items_in_random_order = models.BooleanField()
    scale = models.FloatField()
    precision = models.StringField(choices=['INTEGERS', 'TWO_DIGITS_AFTER_POINT'])
    slider_init = models.StringField(choices=['LEFT', 'RIGHT', 'RAND', 'AVG'])

    def creating_session(self):
        self.select_items = self.session.config['select_items'].upper()
        self.items_in_random_order = self.session.config['items_in_random_order']
        self.scale = float(self.session.config['scale'])
        self.precision = self.session.config['precision'].upper()
        self.slider_init = self.session.config['slider_init'].upper()
        item_order = list(range(1, 7))
        self.set_item_orders(item_order)
        for p in self.get_players():
            p.participant.vars["payoff_svo"] = ""
            p.participant.vars["payoff_svo_other"] = ""

    # Sets the order of items that is going to be shown to each player
    # it can be random for each player or the fixed order according to the paper
    def set_item_orders(self, item_order):
        for player in self.get_players():
            if self.items_in_random_order:
                random.shuffle(item_order)
            player.random_order1 = item_order[0]
            player.random_order2 = item_order[1]
            player.random_order3 = item_order[2]
            player.random_order4 = item_order[3]
            player.random_order5 = item_order[4]
            player.random_order6 = item_order[5]


class Group(BaseGroup):
    pass
    # create a dictionary from the selected values


class Player(BasePlayer):
    payoff_svo = models.StringField()
    payoff_svo_other = models.StringField()
    input_self_1 = models.FloatField()
    input_other_1 = models.FloatField()

    # Same as above but for item 2 in the paper
    input_self_2 = models.FloatField()
    input_other_2 = models.FloatField()
    # Same as above but for item 3 in the paper
    input_self_3 = models.FloatField()
    input_other_3 = models.FloatField()
    # Same as above but for item 2 in the paper and so on.
    input_self_4 = models.FloatField()
    input_other_4 = models.FloatField()
    input_self_5 = models.FloatField()
    input_other_5 = models.FloatField()
    input_self_6 = models.FloatField()
    input_other_6 = models.FloatField()
    input_self_7 = models.FloatField()
    input_other_7 = models.FloatField()
    input_self_8 = models.FloatField()
    input_other_8 = models.FloatField()
    input_self_9 = models.FloatField()
    input_other_9 = models.FloatField()
    input_self_10 = models.FloatField()
    input_other_10 = models.FloatField()
    input_self_11 = models.FloatField()
    input_other_11 = models.FloatField()
    input_self_12 = models.FloatField()
    input_other_12 = models.FloatField()
    input_self_13 = models.FloatField()
    input_other_13 = models.FloatField()
    input_self_14 = models.FloatField()
    input_other_14 = models.FloatField()
    input_self_15 = models.FloatField()
    input_other_15 = models.FloatField()

    # order of item 1 in RANDOM order
    random_order1 = models.IntegerField(initial=-1)
    random_order2 = models.IntegerField(initial=-1)
    random_order3 = models.IntegerField(initial=-1)
    random_order4 = models.IntegerField(initial=-1)
    random_order5 = models.IntegerField(initial=-1)
    random_order6 = models.IntegerField(initial=-1)
    random_order7 = models.IntegerField(initial=-1)
    random_order8 = models.IntegerField(initial=-1)
    random_order9 = models.IntegerField(initial=-1)
    random_order10 = models.IntegerField(initial=-1)
    random_order11 = models.IntegerField(initial=-1)
    random_order12 = models.IntegerField(initial=-1)
    random_order13 = models.IntegerField(initial=-1)
    random_order14 = models.IntegerField(initial=-1)
    random_order15 = models.IntegerField(initial=-1)
    svo_angle = models.FloatField()
    alpha = models.FloatField()
    svo_type = models.StringField(choices=['Altruist', 'Prosocial', 'Individualist', 'Competitive'])
    paid_slider = models.IntegerField(initial=-1)

    #
    #     def sum(self):
    #   mean_to_self = 0
    #   mean_to_others = 0
    #   mean_to_self += Player.input_self_1
    #   mean_to_self += Player.input_self_2
    #   mean_to_self += Player.input_self_3
    #   mean_to_self += Player.input_self_4
    #   mean_to_self += Player.input_self_5
    #   mean_to_self += Player.input_self_6
    #   mean_to_self = mean_to_self / 6
    #   mean_to_others += Player.input_other_1
    #   mean_to_others += Player.input_other_2
    #   mean_to_others += Player.input_other_3
    #   mean_to_others += Player.input_other_4
    #   mean_to_others += Player.input_other_5
    #   mean_to_others += Player.input_other_6
    #   mean_to_others = mean_to_others / 6

    #   svo_angle = degrees(atan((float(mean_to_others) - self.subsession.scale * 50) / (
    #           float(mean_to_self) - self.subsession.scale * 50)))  # Calculate the SVO angle

    #   if self.svo_angle > 57.15:
    #       Player.svo_type = 'Altruist'
    #   elif 57.15 >= self.svo_angle > 22.45:
    #       Player.svo_type = 'Prosocial'
    #   elif 22.45 >= self.svo_angle > -12.04:
    #       Player.svo_type = 'Individualist'
    #   elif self.svo_angle <= -12.04:
    #       Player.svo_type = 'Competitive'

    def set_payoffs(self):
        import random
        rand = random.randint(0, 5)
        self.paid_slider = rand + 1
        self.participant.vars["paid_slider"]=self.paid_slider
        if rand == 0:
            self.participant.vars["payoff_svo"] = str(self.input_self_1)
            self.participant.vars["payoff_svo_other"] = str(self.input_other_1)
        elif rand == 1:
            self.participant.vars["payoff_svo"] = str(self.input_self_2)
            self.participant.vars["payoff_svo_other"] = str(self.input_other_2)
        elif rand == 2:
            self.participant.vars["payoff_svo"] = str(self.input_self_3)
            self.participant.vars["payoff_svo_other"] = str(self.input_other_3)
        elif rand == 3:
            self.participant.vars["payoff_svo"] = str(self.input_self_4)
            self.participant.vars["payoff_svo_other"] = str(self.input_other_4)
        elif rand == 4:
            self.participant.vars["payoff_svo"] = str(self.input_self_5)
            self.participant.vars["payoff_svo_other"] = str(self.input_other_5)
        elif rand == 5:
            self.participant.vars["payoff_svo"] = str(self.input_self_6)
            self.participant.vars["payoff_svo_other"] = str(self.input_other_6)
        self.payoff_svo = self.participant.vars["payoff_svo"]
        self.payoff_svo_other=self.participant.vars["payoff_svo_other"]