from backbone_classes import *
import copy

class PlotFragment:
    def __init__(self):
        self.drama = 5
        return

    def checkPreconditions(self, worldstate):
        """ return a boolean if the event can happen,
        the characters involved, environments, and the updated drama score"""
        return

    def doEvent(self, worldstate, characters, environment):
        return

    def getNewWorldstate(self, worldstate, characters, environment):
        return


class VentThroughAirlock(PlotFragment):
    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []

        indexOfSpace = 0
        for environment in worldstate.environments:
            if environment.name == "Space":
                space = environment
                indexOfSpace = worldstate.environments.index(space)
                #print("Index of space found: ")
                #print(indexOfSpace)
        for character in worldstate.characters:
            if character.location.has_airlock:
                for character2 in character.relationships:
                    if (character.relationships[character2] < 0) & character.sameLoc(character2):
                        valid_characters.append([character, character2])
                        environments.append(worldstate.environments[indexOfSpace])

        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment):
        reachable_worldstate = copy.deepcopy(worldstate)
        print("{} pushes {} out of the airlock.".format(characters[0].name, characters[1].name))
        reachable_worldstate.characters[worldstate.characters.index(characters[1])].location = reachable_worldstate.environments[worldstate.environments.index(environment)] #Change this in the future, environment is a copy (bc deepcopy)
        return reachable_worldstate

    def getNewWorldState(self, worldstate, characters, environment):
        reachable_worldstate = copy.deepcopy(worldstate)
        reachable_worldstate.characters[worldstate.characters.index(characters[1])].location = environment #Change this in the future, environment is a copy (bc deepcopy)
        return reachable_worldstate


class FallInLove(PlotFragment):
    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        for character in worldstate.characters:
                for character2 in character.relationships:
                    if (character.relationships[character2] > 0) & character.sameLoc(character2):
                        valid_characters.append([character, character2])
                        environments.append([])

        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment):
        reachable_worldstate = copy.deepcopy(worldstate)
        print("{} looks at {} and realizes they have been slowly growing attached to them as they have spent time together. They feel a stronger desire to be around them".format(characters[0].name, characters[1].name))
        char_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char = reachable_worldstate.characters[char_index]
        char_two = reachable_worldstate.characters[char_two_index]
        print(str(char.name) + "'s relationship towards " + str(char_two.name) + " was: ")
        print(char.relationships[char_two])
        print("and is now: ")
        char.updateRelationship(char_two, 15)
        print(char.relationships[char_two])
        return reachable_worldstate

    def getNewWorldState(self, worldstate, characters, environment):
        reachable_worldstate = copy.deepcopy(worldstate)
        char_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char = reachable_worldstate.characters[char_index]
        char_two = reachable_worldstate.characters[char_two_index]
        char.updateRelationship(char_two, 15)
        return reachable_worldstate


class GetJob(PlotFragment):
    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        for character in worldstate.characters:
            if not (character.has_job or character.fugitive):
                valid_characters.append([character])
        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments
    
    def doEvent(self, worldstate, characters, environment):
        reachable_worldstate = copy.deepcopy(worldstate)
        print("After trying on dozens of business casual outfits and suffering through ", \
            "awkward interviews, {} got a job.".format(characters[0].name))
        char_index = worldstate.characters.index(characters[0])
        char = reachable_worldstate.characters[char_index]
        prev_char = worldstate.characters.index(char_index)
        char.updateHealth(2)
        char.updateHappiness(4)
        print(str(char.name) + "'s health was {} and is now {}.".format(prev_char.health, char.health))
        print(str(char.name) + "'s happiness was {} and is now {}.".format(prev_char.happiness, char.happiness))
        return reachable_worldstate
    
    def getNewWorldstate(self, worldstate, characters, environment):
        reachable_worldstate = copy.deepcopy(worldstate)
        char_index = worldstate.characters.index(characters[0])
        char = reachable_worldstate.characters[char_index]
        char.updateHealth(2)
        char.updateHappiness(4)
        return reachable_worldstate


class HitBySpaceCar(PlotFragment):
    """ 
    My roommates say if they hit someone with a spacecar, they'd
    be more inclined towards being kind to that person. So the driver's
    relationship to the victim will go up, and the victim's relationship to
    the driver will go down.
    """

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        for character in worldstate.characters:
                for character2 in worldstate.characters:
                    if character != character2:
                        valid_characters.append([character, character2])
                        environments.append([])
        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment):
        reachable_worldstate = copy.deepcopy(worldstate)
        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]
        prev_char_one = worldstate.characters[char_one_index]
        prev_char_two = worldstate.characters[char_two_index]
        char_one.updateRelationship(char_two, 2)
        char_two.updateRelationship(char_one, -10)
        char_two.updateHealth(-6)
        print("{} hits {} with their spacecar.".format(char_one.name, char_two.name))
        if char_two.health == 0:  # kill character
            for character in reachable_worldstate:
                if char_two in character.relationships:
                    del character.relationships[char_one]
            reachable_worldstate.characters.remove(char_one)
            print("As {} lay there on the spaceway, they stared up at two moons rising over the dusky" \
                " horizon. Then they closed their eyes for the last time.".format(char_two.name)) 
            char_two.murderer = True
        else:
            print("{}'s relationship towards {} was {} and is now {}.".format(char_one.name, char_two.name, \
                prev_char_one.relationships[prev_char_two], char_one.relationships[char_two]))
            print("{}'s relationship towards {} was {} and is now {}.".format(char_two.name, char_one.name, \
                prev_char_two.relationships[prev_char_one], char_two.relationships[char_one]))
            print("{}'s health is now {}.".format(char_two.name, char_two.health))
        return reachable_worldstate
    
    def getNewWorldstate(self, worldstate, characters, environment):
        reachable_worldstate = copy.deepcopy(worldstate)
        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]
        if char_one.health == 0:  # kill character
            for character in reachable_worldstate:
                if char_one in character.relationships:
                    del character.relationships[char_one]
            reachable_worldstate.characters.remove(char_one)
        else:
            char_one.updateRelationship(char_two, 2)
            char_two.updateRelationship(char_one, -10)
        return reachable_worldstate


class GoToSpaceJail(PlotFragment):
    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        for character in worldstate.characters:
            if (character.stole or character.exploited or character.murderer or character.fugitive):
                valid_characters.append([character])
        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments
    
    def doEvent(self, worldstate, characters, environment):
        reachable_worldstate = copy.deepcopy(worldstate)
        char_index = worldstate.characters.index(characters[0])
        char = reachable_worldstate.characters[char_index]
        prev_char = worldstate.characters.index(char_index)
        char.updateHappiness(-5)
        print("The law finally caught up with {}. They are in jail.".format(characters[0].name))
        print(str(char.name) + "'s happiness was {} and is now {}.".format(prev_char.happiness, char.happiness))
        self.sendCharacterToJail(char)
        return reachable_worldstate
    
    def getNewWorldstate(self, worldstate, characters, environment):
        reachable_worldstate = copy.deepcopy(worldstate)
        char_index = worldstate.characters.index(characters[0])
        char = reachable_worldstate.characters[char_index]
        char.updateHappiness(-5)
        self.sendCharacterToJail(char, reachable_worldstate)
        return reachable_worldstate
    
    def sendCharacterToJail(character, worldstate):
        jail = False
        for location in worldstate.environments:
            if location.name == "Space Jail":
                jail = location
        if not jail:
            jail = Environment("Space Jail", -2, False, True) 
            worldstate.environments.append(jail)
        character.location = jail