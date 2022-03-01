from backbone_classes import *
from events import *
from path_finding import *

def getRunableEvents(current_worldstate, possible_events):
    runableEvents = []
    for event in possibleEvents: # Check to see if an instance of an event is runnable
        preconditions_met, characters, environments = event.checkPreconditions(current_worldstate)
        if preconditions_met: # If so, add all possible instances to the list of runnable events
            for x in range(len(characters)):
                runableEvents.append([event, current_worldstate, characters[x], environments[x]])
    return runableEvents


def runStory(current_worldstate, possible_events, depth_limit, waypoint = None):
    if (depth_limit == 0):
        return
    
    runable_events = getRunableEvents(current_worldstate, possible_events)
    if len(runable_events) == 0:
        print("No more events are possible. Fin.")
        return

    # Setup to get story to pathfind to the first waypoint.
    if waypoint != None:
        desired_world_state = waypoint
    else:
        desired_world_state = copy.deepcopy(current_worldstate) # TODO: Replace this with an actual goal worldstate

    idx_of_event_to_run = selectEventIndex(runable_events, desired_world_state)
    event = runable_events[idx_of_event_to_run][0]
    worldstate_to_run = runable_events[idx_of_event_to_run][1]
    chars_to_use = runable_events[idx_of_event_to_run][2]
    environments_to_use = runable_events[idx_of_event_to_run][3]
    next_worldstate = event.doEvent(worldstate_to_run, chars_to_use, environments_to_use)

    runStory(next_worldstate, possible_events, depth_limit-1)
    return


if __name__ == "__main__":
    # Environment Initialization
    serenity = Environment("Serenity", 25, False, True)
    space = Environment("Space", -100, True, False)
    serenity.setDistance(space, 0)
    space.setDistance(serenity, 0)

    # Character & Relationship Initialization
    jess = Character("Jess", health=10, happiness=0, location=serenity)
    mal = Character("Mal", health=10, happiness=0, location=serenity)
    jess.updateRelationship(mal, -15)
    mal.updateRelationship(jess, 25)

    environments = [serenity, space]
    characters = [jess, mal]

    initialState = WorldState(0, characters, environments)
    updateState = WorldState(1, [Character("Jess", health=12)], environments)


    loveEvent = FallInLove()
    #preconditions_met, characters, environments = loveEvent.checkPreconditions(initialState)
    #if preconditions_met:
    #    next_worldstate = loveEvent.doEvent(initialState, characters[0], environments)

    airlockEvent = VentThroughAirlock()
    #preconditions_met, characters = airlockEvent.checkPreconditions(initialState)
    #if preconditions_met:
    #    next_worldstate = airlockEvent.doEvent(initialState, characters[0], space)


    possibleEvents = [loveEvent, airlockEvent, HitBySpaceCar(), GetJob()]

    runStory(initialState, possibleEvents, 5, updateState)
    #print(distanceBetweenWorldstates(initialState, updateState))


