from CollegeRuled import *
import copy

class PlotFragment:
    def __init__(self):
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
        for character in worldstate.characters:
            if character.location.has_airlock:
                for character2 in character.relationships:
                    if (character.relationships[character2] < 0) & character.sameLoc(character2):
                        valid_characters.append([character, character2])
                        environments.append([])

        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment):
        reachable_worldstate = copy.deepcopy(worldstate)
        reachable_worldstate.index += 1
        print("{} pushes {} out of the airlock.".format(characters[0].name, characters[1].name))
        reachable_worldstate.characters[worldstate.characters.index(characters[1])].location = environment #Change this in the future, environment is a copy (bc deepcopy)
        return reachable_worldstate

    def getNewWorldState(self, worldstate, characters, environment):
        reachable_worldstate = copy.deepcopy(worldstate)
        reachable_worldstate.index += 1
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
        reachable_worldstate.index += 1
        print("{} looks at {} and realizes they have been slowly growing attached to them as they have spent time together. They feel a stronger desire to be around them".format(characters[0].name, characters[1].name))
        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]
        print(str(char_one.name) + "'s relationship towards " + str(char_two.name) + " was: ")
        print(char_one.relationships[char_two])
        print("and is now: ")
        char_one.relationships[char_two] += 15 #Change this in the future, environment is a copy (bc deepcopy)
        print(char_one.relationships[char_two])
        return reachable_worldstate

    def getNewWorldState(self, worldstate, characters, environment):
        reachable_worldstate = copy.deepcopy(worldstate)
        #print("{} looks at {} and realizes they have been slowly growing attached to them as they have spent time together. They feel a stronger desire to be around them".format(characters[0].name, characters[1].name))
        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]
        #print(char_one.relationships[char_two])
        char_one.relationships[char_two] += 15 #Change this in the future, environment is a copy (bc deepcopy)
        #print(char_one.relationships[char_two])
        return reachable_worldstate