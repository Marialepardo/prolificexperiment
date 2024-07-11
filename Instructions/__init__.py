from otree.api import *
import random
import pandas as pd
from collections import Counter
from numpy import random as rnd
import numpy as np
doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL         = 'Intro'
    PLAYERS_PER_GROUP   = None
    NUM_ROUNDS          = 1
    # Setup/Experiment variables 
    iPracticeRounds     = 3
    iOptions            = 38 #27 options? = trial
    # iNumTrials          = 5
    iNumTrials          = iPracticeRounds + 3*iOptions
    # Template variables
    AvgDur              = '15'
    iBonus              = '1.5 euros'
    ## Symbols directory 
    example_control = "global/figures/example_control.GIF"
    example_price_prime = "global/figures/example_price_prime.gif"
    example_sus_prime = "global/figures/example_sus_prime.gif"

    carbon_green       = "global/figures/carbon/carbon_1.png"
    carbon_red      = "global/figures/carbon/carbon_3.png"
    circled_task = "global/figures/circled.png"

    # Links 
    # You might want to have different links, for when they submit different answers
    sLinkReturn         = "https://app.prolific.com/submissions/complete?cc=XXXXX"
    sLinkReturnCal      = "https://app.prolific.com/submissions/complete?cc=YYYYY"
    sLinkOtherBrowser   = "https://YOUR-EXPERIMENT.herokuapp.com/room/room1"
    SubmitLink          = 'https://app.prolific.com/submissions/complete?cc=ZZZZZ'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    pass
    sTreesLocation = models.StringField() 

# FUNCTIONS
    #Here we randomize the treatments 
def creating_session(subsession):
    # Load Session variables
    s = subsession.session 
    if subsession.round_number == 1:
        for player in subsession.get_players():
            # Store any treatment variables or things that stay constant across rounds/apps
            p = player.participant
            # When creating the session, you can define whether you have a random treatment or a specific one. 
            if s.config['treatment']=='random':
                p.sTreatment = random.choice(['price_prime','sustainability_prime','control'])
            else:
                p.sTreatment = s.config['treatment']
            # Randomly selected trial
            p.iSelectedTrial = random.randint(C.iPracticeRounds,C.iNumTrials)
            ## LOAD HERE YOUR DATABASE 


# PAGES


class Instructions(Page):
    form_model = 'player'

    @staticmethod
    def js_vars(player: Player):
        ## Variables necessary for javascript
        p = player.participant
        return dict(
            lSolutions = [
                'a','c', '3', str(C.iPracticeRounds) # Solutions to control questions
            ]
        )
    
    @staticmethod
    #Here we define variables that will be called in the html file. This one is used to define slide 4 of the instructions with the correct png. examples
    def vars_for_template(player: Player):
        p = player.participant
        return dict(  
            control= p.sTreatment =="control",
            price_prime=p.sTreatment =="price_prime"

        )


page_sequence = [Instructions]
