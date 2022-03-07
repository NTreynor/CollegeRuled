from backbone_classes import *
from events import *
from law_events import *
from love_events import *
from health_events import *
from path_finding import *

def getRunableEvents(current_worldstate, possible_events):
    runableEvents = []
    for event in possible_events: # Check to see if an instance of an event is runnable
        preconditions_met, characters, environments = event.checkPreconditions(current_worldstate)
        if preconditions_met: # If so, add all possible instances to the list of runnable events
            for x in range(len(characters)):
                runableEvents.append([event, current_worldstate, characters[x], environments[x]])
    return runableEvents


def runStory(current_worldstate, possible_events, depth_limit, waypoint = None):
    if (depth_limit == 0):
        return current_worldstate
    
    runable_events = getRunableEvents(current_worldstate, possible_events)
    if len(runable_events) == 0:
        print("THE END")
        return current_worldstate

    # Setup to get story to pathfind to the first waypoint.
    if waypoint != None:
        desired_world_state = waypoint
    else:
        desired_world_state = copy.deepcopy(current_worldstate) # TODO: Replace this with an actual goal worldstate

    #idx_of_event_to_run = selectEventIndex(runable_events, desired_world_state)[0]
    idx_of_event_to_run = getBestIndexLookingAhead(3, runable_events, desired_world_state, possible_events)[0] #First parameter indicates search depth. Do not exceed 6.
    event = runable_events[idx_of_event_to_run][0]
    worldstate_to_run = runable_events[idx_of_event_to_run][1]
    chars_to_use = runable_events[idx_of_event_to_run][2]
    environments_to_use = runable_events[idx_of_event_to_run][3]
    next_worldstate = event.doEvent(worldstate_to_run, chars_to_use, environments_to_use)

    return runStory(next_worldstate, possible_events, depth_limit-1)


if __name__ == "__main__":
    # Environment Initialization
    serenity = Environment("Serenity", 25, False, True)
    space = Environment("Space", -100, True, False)
    serenity.setDistance(space, 0)
    space.setDistance(serenity, 0)

    # Character & Relationship Initialization
    jess = Character("Jess", health=7, happiness=10, location=serenity)
    mal = Character("Mal", health=5, happiness=10, location=serenity)
    inara = Character("Inara", health=10, happiness=0, location=serenity)

    jess.updateRelationship(mal, 45)
    mal.updateRelationship(jess, 45)
    inara.updateRelationship(jess, 45)
    inara.updateRelationship(mal, 45)

    happy_jess = Character("Jess", happiness=10, location=serenity)
    happy_mal = Character("Mal", happiness=10, location=serenity)
    heartbroken_inara = Character("Inara", happiness=0, location=serenity)

    happy_jess.updateRelationship(happy_mal, 90)
    happy_mal.updateRelationship(happy_jess, 90)

    loveChars = [happy_mal, happy_jess, heartbroken_inara]


    environments = [serenity, space]
    characters = [jess, mal, inara]

    initialState = WorldState(0, characters, environments)

    # Creating new characters for a more interesting waypoint.

    new_jess = Character("Jess", health=2, happiness=0, location=serenity)
    new_mal = Character("Mal", health=2, happiness=0, location=serenity)
    new_inara = Character("Inara", health=2, happiness=9, location=serenity)
    new_jess.updateRelationship(new_mal, 35)
    new_mal.updateRelationship(new_jess, -25)
    new_inara.updateRelationship(new_jess, 60)
    new_inara.updateRelationship(new_mal, -50)
    newChars = [new_mal, new_jess, new_inara]

    #updateState = WorldState(1, [Character("Jess", health=2)], environments)
    updateState = WorldState(1, newChars, environments)
    loveState = WorldState(1, loveChars, environments)


    possibleEvents = [FallInLove(), AskOnDate(),  HitBySpaceCar(), GetMiningJob(), 
                        GetSpaceShuttleJob(), GoToSpaceJail(), SoloJailbreak(), CoffeeSpill(),
                        HospitalVisit(), Cheat()]

    loveEvents = [FallInLove(), AskOnDate(), Cheat()]
    #loveEvents = [FallInLove(), Cheat()]
    simpleTest = [FallInLove()]

    #runStory(initialState, loveEvents, 5, updateState)
    #runStory(initialState, simpleTest, 5, updateState)
    #print(distanceBetweenWorldstates(initialState, updateState))

    "TALE OF WOE AND MISERY:"
    #runStory(initialState, possibleEvents, 10, updateState)

    "TALE OF LOVE AND DRAMA:"
    finalState = runStory(initialState, loveEvents, 5, loveState)

    print("Starting Distance: ")
    print(distanceBetweenWorldstates(initialState, loveState))

    print("Final Distance: ")
    print(distanceBetweenWorldstates(finalState, loveState))


