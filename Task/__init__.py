from otree.api import *
import numpy.random as rnd  
import random 
import pandas as pd 

doc = """
Your app description
"""

class C(BaseConstants): #app’s parameters and constants that do not vary from player to player.
    NAME_IN_URL = 'Task'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 41
    NUM_PROUNDS = 3
    
    # Images 
    carbon      = "global/figures/carbon/carbon_"
    price       = "global/figures/price/price_"
    items       = "global/figures/items/items_"

    ##OLD CODE 
    lAttrID     = ['i','p','s']
    lAttrNames  = ['Product','Price','Sustainability']
    # Template vars
    lColNames   = ['Product A','Product B']


    # In between round messages
    BetweenTrialMessages = {
        "1": f"Now you will have {NUM_PROUNDS} practice rounds.", 
        str(int(NUM_PROUNDS+1)): "The practice rounds are over."
        }


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer): #Here we fill out our data model (table) for our players 
    # DVs
    sChoice     = models.StringField()
    dRT_dec     = models.FloatField()

    # 
    I1=models.IntegerField() #item 1
    I2=models.IntegerField() #item 2
    P1=models.IntegerField() #price 1
    P2=models.IntegerField() #price 2
    S1=models.IntegerField() #sustainability 1
    S2=models.IntegerField() #sustainability 2

    # Attention variables
    sNames      = models.LongStringField(blank=True) 
    sDT         = models.LongStringField(blank=True)
    timedelay   = models.FloatField(blank=True) #timedelay for treatment conditions 

    # # Timestamps
    sStartDec   = models.StringField()
    sEndDec     = models.StringField()
    sStartCross = models.StringField()
    sEndCross   = models.StringField()

    # Others 
    sBetweenBtn = models.StringField() #the 'continue' button between rounds 
    lRoundOrder = models.StringField() # To store the randomized round order
    treatment   = models.StringField() # To store treatment 
    lPos        = models.StringField() # To store counterbalancing 

def creating_session(subsession):
    # Load Session variables
    s = subsession.session #making s variable to improve readability  
    if subsession.round_number == 1: #if practice 
        for player in subsession.get_players():
            p = player.participant #setting treatment on participant not player 
            
    #Counterbalancing the order of attributes
        # Attributes
            attr_pairs = [('i', 'Product'), ('p', 'Price'), ('s', 'Sustainability')]
        
        # Shuffle the pairs except the first one
            fixed_pair = attr_pairs[0]
            shuffle_pairs = attr_pairs[1:]
            random.shuffle(shuffle_pairs)
        
        # Combine the fixed pair with the shuffled pairs
            combined_pairs = [fixed_pair] + shuffle_pairs
        
        # Unzip the pairs into lAttrID and lAttrNames
            lAttrID, lAttrNames = zip(*combined_pairs)
        
        # Convert tuples back to lists
            p.session.vars['lAttrID'] = list(lAttrID)
            p.session.vars['lAttrNames'] = list(lAttrNames)

         # Create hard copy of attributes (price and sustainability)
            lPos = list(lAttrID)  #C.lAttrID[:]
            #random.shuffle(lPos)        # Shuffle order 
            p.lPos = lPos               # Store it as a participant variable
            print(f"position of attributes: {p.lPos}")
            #### Select trial for payment (from the first round after practice rounds to the last)
            #p.iSelectedTrial = random.randint(C.NUM_PROUNDS+1,C.NUM_ROUNDS)
           
           # This is not necessary! You can just call upon it once (in the informed consent)
           #randomizing assignment to one of the three conditions 
            if s.config['treatment']=='random':
                p.sTreatment = random.choice(['price_prime','sustainability_prime','control'])
                print(f"Treatment assigned randomly: {p.sTreatment}")  # Print the randomly assigned treatment
            else:
                p.sTreatment = s.config['treatment']
                print(f"Treatment assigned from config: {p.sTreatment}")  # Print the treatment from config
            
            # Define the practice and real rounds
            practice_rounds = list(range(1, C.NUM_PROUNDS + 1))
            real_rounds = list(range(C.NUM_PROUNDS + 1, C.NUM_ROUNDS + 1))
            
            # Randomize the real rounds
            random.shuffle(real_rounds)
            
            # Combine practice and real rounds
            combined_rounds = practice_rounds + real_rounds
            p.lRoundOrder = ','.join(map(str, combined_rounds))
            print(f"Round order for participant {p.id_in_session}: {p.lRoundOrder}")


        #fix values     
    lValuesMap = { 
    # nuts
    4: [1, 2, 1, 0, 1, 2], 5: [1, 2, 2, 0, 1, 2], 6: [2, 1, 0, 3, 2, 1], 7: [1, 2, 4, 0, 1, 2],
    8: [3, 2, 0, 1, 3, 2], 9: [3, 2, 0, 2, 3, 2], 10: [2, 3, 3, 0, 2, 3], 11: [2, 3, 4, 0, 2, 3],
    12: [3, 1, 0, 1, 3, 1], 13: [3, 1, 0, 2, 3, 1], 14: [1, 3, 3, 0, 1, 3], 15: [1, 3, 4, 0, 1, 3],
    # sweets
    16: [5, 4, 5, 6, 5, 4], 17: [4, 5, 7, 5, 4, 5], 18: [5, 4, 5, 8, 5, 4], 19: [4, 5, 9, 5, 4, 5],
    20: [6, 5, 5, 6, 6, 5], 21: [5, 6, 7, 5, 5, 6], 22: [6, 5, 5, 8, 6, 5], 23: [5, 6, 9, 5, 5, 6],
    24: [6, 4, 5, 6, 6, 4], 25: [4, 6, 7, 5, 4, 6], 26: [6, 4, 5, 8, 6, 4], 27: [4, 6, 9, 5, 4, 6],
    # muesli
    28: [8, 7, 10, 11, 8, 7], 29: [8, 7, 10, 12, 8, 7], 30: [8, 7, 10, 13, 8, 7], 31: [7, 8, 14, 10, 7, 8],
    32: [8, 9, 11, 10, 8, 9], 33: [9, 8, 10, 12, 9, 8], 34: [8, 9, 13, 10, 8, 9], 35: [9, 8, 10, 14, 9, 8],
    36: [9, 7, 10, 11, 9, 7], 37: [7, 9, 12, 10, 7, 9], 38: [9, 7, 10, 13, 9, 7], 39: [9, 7, 10, 14, 9, 7],
    40: [3, 1, 1, 0, 3, 1], 41: [7, 9, 10, 11, 7, 9]
}

    for player in subsession.get_players():
        p = player.participant
        player.sBetweenBtn = random.choice(['left', 'right']) #Randomly assign 'left' or 'right' to sBetweenBtn
        player.treatment = p.sTreatment #this to save treatment condition
        player.lRoundOrder = p.lRoundOrder #this to save round order
        #player.lPos = p.lPos #save counterbalancing
        player.lPos = ','.join(p.lPos)  # Convert list to a comma-separated string


        current_round = subsession.round_number
        lRoundOrder = list(map(int, p.lRoundOrder.split(',')))
        randomized_round = lRoundOrder[current_round - 1]

        if player.round_number <= C.NUM_PROUNDS: 
            # Practice Trials
            print(player.round_number, "practice")  
            if player.round_number == 1:
                lValues = [1,2, 2,0, 1,2] #Preset values for round 1 
            elif player.round_number == 2:
                lValues = [4,5, 3,0, 2,3] #Preset values for round 2 
            elif player.round_number == 3:
                lValues = [8,9, 4,0, 3,4] #Preset values for round 3 
        else:
            print(player.round_number, "normal") #normal rounds randomized 
            if randomized_round in lValuesMap:
                lValues = lValuesMap[randomized_round]
                print(f"Round {current_round} (Randomized to {randomized_round}): {lValues}") 
            else: lValues = [1,1,1,1,1,1] # Default in case of missing key

        player.I1, player.I2, player.P1,player.P2, player.S1,player.S2 = lValues
    
def attributeList(lValues,lPos,Treat):
    lAttributes = []
    lOrder = []

    for i in range(len(C.lAttrID)): #where lAttrID = ['p','s']
        id                  = C.lAttrID[i]      
        name                = C.lAttrNames[i]

        # Store the order of the list
        lOrder.append(lPos.index(id))
        lPaths = [] #Creates an empty list lPaths to store image paths.
        for v in lValues[i]:
            if id=="s":  #iterates through carbon label folders 
                 lPaths.append(f"{C.carbon}{v}.png") #carbon label folder
            elif id=="p":
                lPaths.append(f"{C.price}{v}.png") #prices folder
            else:
                lPaths.append(f"{C.items}{v}.png") #items folder


        # Create object with all the relevant variables
        Attr = {
            'id'        : id,
            'name'      : name,
            'lValues'   : lPaths,
            #'is_price': is_price  # Include price identification (important for HTML template)
        }
        lAttributes.append(Attr)
    
    lFinal = [ lAttributes[x] for x in lOrder]
    return lFinal





# PAGES
class Decision(Page):
    form_model      = 'player'
    form_fields     = ['sStartDec','sEndDec', 'dRT_dec', 'sNames', 'sDT' , 'sChoice', 'timedelay'] #'dTime2first'
    
    @staticmethod
    def vars_for_template(player: Player): # vars_for_template passes variables to the template so you can access them there
        # Order of attributes (from participant var)
        p = player.participant
        lPos = p.lPos
        treatment=p.sTreatment

      
        lValues = [[player.I1,player.I2],[player.P1,player.P2],[player.S1,player.S2]]
        print(lValues)
        return dict(
            lAttr = attributeList(lValues,lPos,treatment),
        )
    
    def get_template_name(player: Player):
        treatment = player.participant.sTreatment
        if treatment == 'price_prime':
            return 'Task/Decision_price_prime.html' #'Task/Decision_price_prime.html' 'Task/Decision_control.html'
        elif treatment == 'sustainability_prime':
            return 'Task/Decision_sus_prime.html' #'Task/Decision_sustainability_prime.html'
        else:
            return 'Task/Decision_control.html'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        p = player.participant
        # Log the values to ensure they are being captured correctly
        print('Before next page values:', {
            'sNames': player.sNames,
            'sDT': player.sDT,
            'sChoice': player.sChoice
        })
        #Maybe add this back in 
        #if player.round_number == p.iSelectedTrial: 
         #   p.bChoseA = player.iChooseB == '0'   
          #  print(f"Decision in selected trial recorded: {p.bChoseA}")
    

class FixCross(Page):
    form_model = 'player'
    form_fields = [ 'sStartCross','sEndCross' ]
    template_name = 'global/FixCross.html'


class SideButton(Page):
    form_model = 'player'
    form_fields = [ 'sStartCross','sEndCross' ]
    template_name = 'global/SideButton.html'

    @staticmethod
    def js_vars(player: Player): #js_vars is used to pass data to JavaScript code in the template
        
        return dict(
            sPosition = player.sBetweenBtn
        )


class Confidence(Page):
    form_model      = 'player'
    #form_fields     = ['sStartConf','sEndConf', 'dRT_conf','iConfidence']
    template_name   = 'global/Confidence.html'
    
    @staticmethod
    def vars_for_template(player: Player):
        p = player.participant
        return dict(
            lScale = list(range(1,C.iLikertConf+1))
        )

class Message(Page):
    template_name = 'global/Message.html'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_PROUNDS
    
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            MessageText = 'The practice rounds ended. <br> The experiment will start now.'
        )

page_sequence = [SideButton, Decision, Message]
#page_sequence = [SideButton, Decision, Confidence]

 