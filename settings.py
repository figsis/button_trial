from os import environ


SESSION_CONFIGS = [
	dict(name='Button',
		 app_sequence=['dat','svo','dana','the_button'],
		 num_demo_participants=100,
		 select_items='PRIMARY',
		 items_in_random_order=False,
		 scale=0.01,
		 slider_init='LEFT',
		 random_payoff='RAND',
		 precision='INTEGERS',
		 doc=''),
	dict(name='Button_nosvo',
		 app_sequence=['dana', 'the_button'],
		 num_demo_participants=100,
		 select_items='PRIMARY',
		 items_in_random_order=False,
		 scale=0.01,
		 slider_init='LEFT',
		 random_payoff='RAND',
		 precision='INTEGERS',
		 doc=''),
]
#DEBUG = False
#DATABASES = {
 #   'default': {
#      'ENGINE': 'django.db.backends.postgresql_psycopg2',
#       'NAME': 'mydb',
#       'USER': 'myuser',
#       'PASSWORD': 'password',
#       'HOST': '',                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
#       'PORT': '',                      # Set to empty string for default.
#   }
#}

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False


ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '2463227021408'

INSTALLED_APPS = ['otree']
