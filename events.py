from CollegeRuled import *
import copy

class VentThroughAirlock(Plotfrag):
    def checkPreconditions(self, worldstate):
        valid_characters = []
        for character in worldstate.characters:
            if character.location.has_airlock:
                for character2 in character.relationships:
                    if (character.relationships[character2] < 0) & character.sameLoc(character2):
                        valid_characters.append([character, character2])

        if valid_characters:
            return True, valid_characters, []
        else:
            return False, None, []

    def doEvent(self, worldstate, characters, environment):
        reachable_worldstate = copy.deepcopy(worldstate)
        reachable_worldstate.index += 1
        print("{} pushes {} out of the airlock.".format(characters[0].name, characters[1].name))
        reachable_worldstate.characters[worldstate.characters.index(characters[1])].location = environment #Change this in the future, environment is a copy (bc deepcopy)
        return reachable_worldstate

    class FallInLove(Plotfrag):
        def checkPreconditions(self, worldstate):
            valid_characters = []
            for character in worldstate.characters:
                    for character2 in character.relationships:
                        if (character.relationships[character2] > 0) & character.sameLoc(character2):
                            valid_characters.append([character, character2])

            if valid_characters:
                return True, valid_characters, []
            else:
                return False, None, []

    def doEvent(self, worldstate, characters, environment):
        reachable_worldstate = copy.deepcopy(worldstate)
        reachable_worldstate.index += 1
        print("{} looks at {} and realizes they have been slowly growing attached to them as they have spent time together. They feel a stronger desire to be around them".format(characters[0].name, characters[1].name))
        char_one_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char_one = reachable_worldstate.characters[char_one_index]
        char_two = reachable_worldstate.characters[char_two_index]
        print(char_one.relationships[char_two])
        char_one.relationships[char_two] += 15 #Change this in the future, environment is a copy (bc deepcopy)
        print(char_one.relationships[char_two])
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
