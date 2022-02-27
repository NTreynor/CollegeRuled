from backbone_classes import *
from events import *

def selectEventIndex(eventList, desiredWorldState):
    #print("attempting to select event index")
    currMinDistanceEventIndex = -1
    currEventMinDistance = 9999
    equallyValubleIndexes = []
    #print(len(eventList))
    for x in range (len(eventList)):
        #print("x = " + str(x))
        currEventValue = distanceBetweenWorldstates(desiredWorldState, eventList[x][0].getNewWorldState(eventList[x][1], eventList[x][2], eventList[x][3]))
        if (currEventValue < currEventMinDistance):
            equallyValubleIndexes = []
            currEventMinDistance = currEventValue
            currMinDistanceEventIndex = x
            equallyValubleIndexes.append(x)
        if (currEventValue == currEventMinDistance):
            equallyValubleIndexes.append(x)

    return random.choice(equallyValubleIndexes) # Return the index of the event with the lowest distance to the desiredWorldState


def distanceBetweenWorldstates(currWorldState, newWorldState):
    #TODO: IMPLEMENT THIS PROPERLY
    #print("Distance between world states is 5")
    return 5


def run_story(worldstate, possibleEvents, depthLimit):
    if (depthLimit == 0):
        return
    runnableEvents = []
    for event in possibleEvents: # Check to see if an instance of an event is runnable
        preconditions_met, characters, environments = event.checkPreconditions(worldstate)
        if preconditions_met: # If so, add all possible instances to the list of runnable events
            #print("length of characters: " + str(len(characters)))
            for x in range(len(characters)):
                #print(x)
                # Store the event, and it's parameters
                runnableEvents.append([event, worldstate, characters[x], environments[x]])

    # Now we would want to select an event to run.
    desiredWorldState = worldstate # TODO: Replace this with an actual goal worldstate
    indexOfEventToRun = selectEventIndex(runnableEvents, desiredWorldState)
    #print(indexOfEventToRun)
    event = runnableEvents[indexOfEventToRun][0]
    worldStateToRun = runnableEvents[indexOfEventToRun][1]
    charsToUse = runnableEvents[indexOfEventToRun][2]
    environmentsToUse = runnableEvents[indexOfEventToRun][3]
    next_worldstate = event.doEvent(worldStateToRun, charsToUse, environmentsToUse)

    run_story(next_worldstate, possibleEvents, depthLimit-1)
    return