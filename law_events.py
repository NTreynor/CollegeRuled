from backbone_classes import *
import copy


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

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        reachable_worldstate.index += 1
        if print_event:
            print("{} pushes {} out of the airlock.".format(characters[0].name, characters[1].name))
        reachable_worldstate.characters[worldstate.characters.index(characters[1])].location = reachable_worldstate.environments[worldstate.environments.index(environment)] #Change this in the future, environment is a copy (bc deepcopy)
        return self.updateEventHistory(reachable_worldstate, characters, environment)


class Steal(PlotFragment):
    def __init__(self):
        self.drama = 7

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        for character in worldstate.characters:
            if character.happiness < 6:
                for character2 in character.relationships:
                    character.updateRelationship(character2, 0)
                    if character.relationships[character2] <= 0:
                        valid_characters.append([character, character2])
                        environments.append([])

        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        thief_idx = worldstate.characters.index(characters[0])
        victim_index = worldstate.characters.index(characters[1])
        thief = reachable_worldstate.characters[thief_idx]
        victim = reachable_worldstate.characters[victim_index]
        if print_event:
            print("{} notices {} forgot to lock up when they left their bunker.".format(thief.name, victim.name),
            "{} breaks in and steals all their valuables.".format(thief.name))
        thief.stole = True
        thief.updateHappiness(4)
        victim.updateHappiness(-4)
        reachable_worldstate.drama_score += self.drama
        return self.updateEventHistory(reachable_worldstate, characters, environment)


class GoToSpaceJail(PlotFragment):
    def __init__(self):
        self.drama = 10

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        if not self.withinRepeatLimit(worldstate, 2):
            return False, None, environments
        for character in worldstate.characters:
            if (character.stole or character.exploited or character.murderer or character.fugitive) \
                and not character.in_jail:
                characters = [character]
                environment = []
                if self.withinRecentHistoryLimit(worldstate, characters, environment, 3):
                    valid_characters.append([character])
                    environments.append([])
        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments
    
    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        char_index = worldstate.characters.index(characters[0])
        char = reachable_worldstate.characters[char_index]
        char.updateHappiness(-5)
        if print_event:
            print("The law finally caught up with {}. They are in space jail.".format(characters[0].name))
        self.sendCharacterToJail(char, reachable_worldstate)
        char.in_jail = True
        reachable_worldstate.drama_score += self.drama
        return self.updateEventHistory(reachable_worldstate, characters, environment)
        
    def sendCharacterToJail(self, character, worldstate):
        jail = False
        for location in worldstate.environments:
            if location.name == "Space Jail":
                jail = location
        if not jail:
            jail = Environment("Space Jail", -2, False, True) 
            worldstate.environments.append(jail)
        character.location = jail


class SoloJailbreak(PlotFragment):
    def init(self):
        self.drama = 15

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        for character in worldstate.characters:
            if character.in_jail:
                valid_characters.append([character])
                environments.append([])
        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        char_index = worldstate.characters.index(characters[0])
        char = reachable_worldstate.characters[char_index]
        char.updateHappiness(3)
        if print_event:
            print("{} spent months chipping at a crack in the circuit panel.".format(characters[0].name), \
                "They finally succeed at shutting down space jail long enough to make a break for it.", \
                "{} returns to their home planet, Higgins.".format(characters[0].name))
        char.in_jail = False
        char.fugitive = True
        reachable_worldstate.drama_score += self.drama
        return self.updateEventHistory(reachable_worldstate, characters, environment)