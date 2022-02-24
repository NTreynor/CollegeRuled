from CollegeRuled import *
import copy

from events import VentThroughAirlock


class Character:
    def __init__(self, name, health, happiness, location):
        self.name = name
        self.health = health # scale of 0 to 10
        self.happiness = happiness # scale of 0 to 10
        self.has_job = False
        self.exploited = False
        self.murderer = False
        self.stole = False
        self.fugitive = False
        self.relationships = {} # key: other character, val: [-100, 100]
        self.romantic_interest = None  # will be the name of the romantic interest
        self.location = location
        # self.in_spacesuit = False

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

    def __str__(self):
        return ""

if __name__ == "__main__":
    serenity = Environment("Serenity", 25, False, True)
    space = Environment("Space", -100, True, False)
    serenity.setDistance(space, 0)
    space.setDistance(serenity, 0)

    jess = Character("Jess", 10, 0, serenity)
    mal = Character("Mal", 10, 0, serenity)
    jess.updateRelationship(mal, -15)
    mal.updateRelationship(jess, 25)

    environments = [serenity, space]
    characters = [jess, mal]

    initialState = WorldState(0, characters, environments)


    loveEvent = VentThroughAirlock()
    preconditions_met, characters, environments = loveEvent.checkPreconditions(initialState)
    if preconditions_met:
        next_worldstate = loveEvent.doEvent(initialState, characters[0], environments)

    #airlockEvent = VentThroughAirlock()
    #preconditions_met, characters = airlockEvent.checkPreconditions(initialState)
    #if preconditions_met:
    #    next_worldstate = airlockEvent.doEvent(initialState, characters[0], space)

