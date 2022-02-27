from backbone_classes import *
from events import *
from path_finding import *

def get_runable_events(current_worldstate, possible_events):
    runableEvents = []
    for event in possibleEvents: # Check to see if an instance of an event is runnable
        preconditions_met, characters, environments = event.checkPreconditions(current_worldstate)
        if preconditions_met: # If so, add all possible instances to the list of runnable events
            for x in range(len(characters)):
                runableEvents.append([event, current_worldstate, characters[x], environments[x]])
    return runableEvents


def run_story(current_worldstate, possibleEvents, depthLimit, waypoints = None):
    if (depthLimit == 0):
        return
    
    runableEvents = get_runable_events(current_worldstate, possibleEvents)
    # Now we would want to select an event to run.
    desiredWorldState = current_worldstate # TODO: Replace this with an actual goal worldstate
    indexOfEventToRun = selectEventIndex(runableEvents, desiredWorldState)
    #print(indexOfEventToRun)
    event = runableEvents[indexOfEventToRun][0]
    worldStateToRun = runableEvents[indexOfEventToRun][1]
    charsToUse = runableEvents[indexOfEventToRun][2]
    environmentsToUse = runableEvents[indexOfEventToRun][3]
    next_worldstate = event.doEvent(worldStateToRun, charsToUse, environmentsToUse)

    run_story(next_worldstate, possibleEvents, depthLimit-1)
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


    loveEvent = FallInLove()
    #preconditions_met, characters, environments = loveEvent.checkPreconditions(initialState)
    #if preconditions_met:
    #    next_worldstate = loveEvent.doEvent(initialState, characters[0], environments)

    airlockEvent = VentThroughAirlock()
    #preconditions_met, characters = airlockEvent.checkPreconditions(initialState)
    #if preconditions_met:
    #    next_worldstate = airlockEvent.doEvent(initialState, characters[0], space)

    possibleEvents = [loveEvent, airlockEvent]

    run_story(initialState, possibleEvents, 5)


