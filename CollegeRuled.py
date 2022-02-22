import copy

from git.exc import GitCommandError
from pydriller import Repository
from pydriller.metrics.process.code_churn import CodeChurn
from pydriller.metrics.process.commits_count import CommitsCount
from datetime import datetime, timedelta, timezone
import pandas as pd
import pytz


class Character:
    def __init__(self, name, happiness, location, in_spacesuit):
        self.name = name
        self.happiness = happiness
        self.location = location
        self.relationships = {}
        self.in_spacesuit = in_spacesuit

    def updateRelationship(self, other_character, friendship_enemy_index):
        self.relationships[other_character] = friendship_enemy_index

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

    def __str__(self):
        return ""

class Plotfrag:
    def __init__(self):
        return

    def checkPreconditions(self, worldstate):
        return

    def doEvent(self, worldstate, characters):
        return

class VentThroughAirlock(Plotfrag):
    def checkPreconditions(self, worldstate):
        valid_characters = []
        for character in worldstate.characters:
            if character.location.has_airlock:
                for character2 in character.relationships:
                    if (character.relationships[character2] < 0) & character.sameLoc(character2):
                        valid_characters.append([character, character2])

        if valid_characters:
            return True, valid_characters
        else:
            return False, None

    def doEvent(self, worldstate, characters, environment):
        reachable_worldstate = copy.deepcopy(worldstate)
        reachable_worldstate.index += 1
        print("{} pushes {} out of the airlock.".format(characters[0].name, characters[1].name))
        reachable_worldstate.characters[worldstate.characters.index(characters[1])].location = environment #Change this in the future, environment is a copy (bc deepcopy)
        return reachable_worldstate




if __name__ == "__main__":
    serenity = Environment("Serenity", 25, False, True)
    space = Environment("Space", -100, True, False)
    serenity.setDistance(space, 0)
    space.setDistance(serenity, 0)

    jess = Character("Jess", 0, serenity, False)
    mal = Character("Mal", 5, serenity, False)
    jess.updateRelationship(mal, -15)
    mal.updateRelationship(jess, 25)

    environments = [serenity, space]
    characters = [jess, mal]

    initialState = WorldState(0, characters, environments)

    airlockEvent = VentThroughAirlock()
    preconditions_met, characters = airlockEvent.checkPreconditions(initialState)
    if preconditions_met:
        next_worldstate = airlockEvent.doEvent(initialState, characters[0], space)


