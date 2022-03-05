class Character:
    def __init__(self, name, health=None, happiness=None, has_job=None, exploited=None, \
        murderer=None, stole=None, in_jail=None, fugitive=None, relationships = None, \
            romantic_partner=None, location=None):
        self.name = name  # string
        self.health = health # scale of 0 to 10
        self.happiness = happiness # scale of 0 to 10
        self.has_job = has_job  # boolean
        self.exploited = exploited  # boolean
        self.murderer = murderer  # boolean
        self.stole = stole  # boolean
        self.in_jail = in_jail # boolean
        self.fugitive = fugitive  # boolean
        self.relationships = relationships # key: other character, val: [-100, 100]
        if relationships == None:
            self.relationships = {}
        self.romantic_partner = romantic_partner  # will be the name of the romantic interest
        self.location = location  # Environment type
        # self.in_spacesuit = False
    
    def getAttributes(self):
        """ for waypointing """
        return [self.health, self.happiness, self.has_job, self.exploited, self.murderer, \
            self.stole, self.in_jail, self.fugitive, self.relationships, self.romantic_partner, self.location]

    def getAttributeDistance(self, attribute_idx, attribute_value):
        if self.getAttributes()[attribute_idx] == None: # Don't do a comparison if one doesn't need to be made.
            return 0
        if attribute_idx in [0, 1]:  # health or happiness
            dist = (self.getAttributes()[attribute_idx] - attribute_value) * 5 
            dist = abs(dist)
        elif attribute_idx in range(2, 8):  # booleans
            dist = 50
            if self.getAttributes()[attribute_idx] == attribute_value:
                dist = 0
        elif attribute_idx == 8:  #  relationships
            dist = 0
            for character in attribute_value:
                if character in self.relationships:
                    char_dist = (self.relationships[character] - attribute_value[character]) * 1/4
                else:
                    char_dist = attribute_value[character] * 1/4  # initialize relationship as 0
                char_dist = abs(dist)
                dist += char_dist
        elif attribute_idx == 9:  # romantic interest
            if self.romantic_partner == attribute_value:
                dist = 0
            else:
                dist = 50
        elif attribute_idx == 10:  # location
            dist = 0
        return dist
    
    def getDistanceToFutureState(self, future_state_attributes):
        """ returns distance between current state of character
        and future state of character"""
        distance = 0
        for idx, attribute in enumerate(future_state_attributes):
            if attribute:
                distance += self.getAttributeDistance(idx, attribute)
        return distance

    def updateRelationship(self, other_character, relationship_change):
        """ 
        change relationship between characters by decreasing
        or increasing value
        @relationship_change: int amount to change relationship by, positive or negative"""
        if other_character in self.relationships.keys():
            current_relationship =  self.relationships[other_character]
            new_relationship = current_relationship + relationship_change
            if abs(new_relationship) > 100:
                new_relationship = 100 * new_relationship/abs(new_relationship)

            self.relationships[other_character] = int(new_relationship)
        else:
            current_relationship =  0
            new_relationship = current_relationship + relationship_change
            if abs(new_relationship) > 100:
                new_relationship = 100 * new_relationship/abs(new_relationship)

            self.relationships[other_character] = int(new_relationship)

    
    def updateHealth(self, health_change):
        """ 
        change health of character
        @health_change: int amount to change health by, positive or negative"""
        new_health = self.health + health_change
        if new_health > 10:
            new_health = 10
        elif new_health < 0:
            new_health = 0
        self.health = new_health
    
    def updateHappiness(self, happiness_change):
        """ 
        change happiness of character
        @happiness_change: int amount to change happiness by, positive or negative"""
        new_happiness = self.happiness + happiness_change
        if new_happiness > 10:
            new_happiness = 10
        elif new_happiness < 0:
            new_happiness = 0
        self.happiness = new_happiness
    
    def isDead(self):
        if self.health == 0:
            return True
        return False

    def sameLoc(self, other_character):
        return self.location == other_character.location

    def __str__(self):
        return "Character name is %s. Relationship matrix is: %s." % (self.name, str(self.relationships))


class Environment:
    def __init__(self, name, quality, spacesuit_needed, has_airlock):
        self.name = name
        self.quality = quality
        self.distances = {}
        self.spacesuit_needed = spacesuit_needed
        self.has_airlock = has_airlock

    def setDistance(self, other_environment, distance_index):
        self.distances[other_environment] = distance_index

    def __str__(self):
        return "Environment name is %s. Distance matrix is: %s." % (self.name, str(self.distances))


# World state should consist of a list of characters and environments.
class WorldState:
    def __init__(self, index, characters, environments):
        self.index = index
        self.characters = characters
        self.environments = environments
        self.drama_score = 0
    
    def removeCharacter(self, character):
        for other_character in self.characters:
                if character in other_character.relationships:
                    del other_character.relationships[character]
        self.characters.remove(character)

    def __str__(self):
        return ""


class PlotFragment:
    def __init__(self):
        self.drama = 0  # out of 20
        return

    def checkPreconditions(self, worldstate):
        """ return a boolean if the event can happen,
        the characters involved, environments, and the updated drama score"""
        return

    def doEvent(self, worldstate, characters, environment, print_event=True):
        return

    def getNewWorldState(self, worldstate, characters, environment):
        return self.doEvent(worldstate, characters, environment, print_event=False)

