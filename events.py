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

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        reachable_worldstate.index += 1
        if print_event:
            print("{} looks at {} and realizes they have been slowly growing attached to them as they have spent time together. They feel a stronger desire to be around them".format(characters[0].name, characters[1].name))
        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]
        char_one.relationships[char_two] += 15
        if print_event:
            print(str(char_one.name) + "'s relationship towards " + str(char_two.name) + " was", \
                char_one.relationships[char_two] - 15, "and is now", str(char_one.relationships[char_two]) + ".")
        return reachable_worldstate


class GetJob(PlotFragment):
    def __init__(self):
        self.drama = 4

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        for character in worldstate.characters:
            if not (character.has_job or character.fugitive):
                valid_characters.append([character])
                environments.append([])
        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments
    
    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        if print_event:
            print("After visiting the open market every day and getting increasingly desperate", \
                "{} got a job.".format(characters[0].name))
        char_index = worldstate.characters.index(characters[0])
        char = reachable_worldstate.characters[char_index]
        char.updateHappiness(4)
        char.has_job = True
        reachable_worldstate.drama_score += self.drama
        return reachable_worldstate
    

class HitBySpaceCar(PlotFragment):
    """ 
    My roommates say if they hit someone with a spacecar, they'd
    be more inclined towards being kind to that person. So the driver's
    relationship to the victim will go up, and the victim's relationship to
    the driver will go down.
    """
    def __init__(self):
        self.drama = 14

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

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]
        char_one.updateRelationship(char_two, 2)
        char_two.updateRelationship(char_one, -10)
        char_two.updateHealth(-6)
        if print_event:
            print("{} hits {} with their spacecar.".format(char_one.name, char_two.name))
        if char_two.isDead():  # kill character
            self.drama += 5  # more dramatic if character dies
            reachable_worldstate.removeCharacter(char_two)
            if print_event:
                print("As {} lay there on the spaceway, they stared up at two moons rising over the dusky" \
                    " horizon. Then they closed their eyes for the last time.".format(char_two.name)) 
            char_one.murderer = True
        reachable_worldstate.drama_score += self.drama
        return reachable_worldstate
    

class GoToSpaceJail(PlotFragment):
    def __init__(self):
        self.drama = 10

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        for character in worldstate.characters:
            if (character.stole or character.exploited or character.murderer or character.fugitive) \
                and not character.in_jail:
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
        prev_char = worldstate.characters[char_index]
        char.updateHappiness(-5)
        if print_event:
            print("The law finally caught up with {}. They are in space jail.".format(characters[0].name))
        self.sendCharacterToJail(char, reachable_worldstate)
        char.in_jail = True
        reachable_worldstate.drama_score += self.drama
        return reachable_worldstate
        
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
        if print_event
            print("{} spent months chipping at a crack in the circuit panel.".format(characters[0].name), \
                "They finally succeed at shutting down space jail long enough to make a break for it.", \
                "{} returns to their home planet, Higgins.".format(characters[0].name))
        char.in_jail = False
        char.fugitive = True
        reachable_worldstate.drama_score += self.drama
        return reachable_worldstate


class CoffeeSpill(PlotFragment):
    def __init__(self):
        self.drama = 3

    def checkPreconditions(self, worldstate):
        valid_characters = []
        environments = []
        for character in worldstate.characters:
            for character2 in character.relationships:
                if character.sameLoc(character2):
                    valid_characters.append([character, character2])
                    environments.append([])

        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        if print_event:
            print("{} is walking along with a fresh cup of hydrozine, and loses their footing right as they would pass by {}, spilling their drink all over them! \"Oh goodness, sorry about that!\" says {}.".format(characters[0].name, characters[1].name, characters[0].name))
        char_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char = reachable_worldstate.characters[char_index]
        char_two = reachable_worldstate.characters[char_two_index]
        prev_relationship = char.relationships[char_two]
        char.updateRelationship(char_two, 5)
        char_two.updateRelationship(char, -5)
        reachable_worldstate.drama_score += self.drama
        return reachable_worldstate