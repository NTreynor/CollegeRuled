from backbone_classes import *
from events import *
from law_events import *
from love_events import *
from health_events import *
import random

from run import getRunableEvents


def selectEventIndex(eventList, desiredWorldState):
    if len(eventList) == 0: # TODO: Handle this before calling it, rather than after.
        print("No events left in this tree!")
        return 0, 9999

    currMinDistanceEventIndex = -1
    currEventMinDistance = 9999
    equallyValubleIndexes = []
    for x in range (len(eventList)):
        reachable_worldstate = eventList[x][0].getNewWorldState(eventList[x][1], eventList[x][2], eventList[x][3])
        currEventValue = distanceBetweenWorldstates(reachable_worldstate, desiredWorldState)

        if (currEventValue < currEventMinDistance):
            equallyValubleIndexes = []
            currEventMinDistance = currEventValue
            currMinDistanceEventIndex = x
        if (currEventValue == currEventMinDistance):
            equallyValubleIndexes.append(x)


    if len(equallyValubleIndexes) >= 1:
        return random.choice(equallyValubleIndexes), currEventMinDistance # Return the index of the event with the lowest distance to the desiredWorldState
    else:
        return 0, 9999

def getBestIndexLookingAhead(depth, eventList, desiredWorldState, possible_events):
    if depth == 1:
        return selectEventIndex(eventList, desiredWorldState)

    if depth >= 2:
        currEventMinDistance = 99999
        equallyValubleIndexes = []

        for x in range (len(eventList)):
            reachable_worldstate = eventList[x][0].getNewWorldState(eventList[x][1], eventList[x][2], eventList[x][3])
            runable_events = getRunableEvents(reachable_worldstate, possible_events)
            currWorldStateValue = getBestIndexLookingAhead(depth-1, runable_events, desiredWorldState, possible_events)

            if (currWorldStateValue[1] < currEventMinDistance):
                equallyValubleIndexes = []
                currEventMinDistance = currWorldStateValue[1]
                equallyValubleIndexes.append(x)

            if (currWorldStateValue[1] == currEventMinDistance):
                equallyValubleIndexes.append(x)

        return random.choice(equallyValubleIndexes), currEventMinDistance



def distanceBetweenWorldstates(currWorldState, newWorldState):
    distance = 0
    if currWorldState.characters:
        for character in currWorldState.characters:
            for future_character in newWorldState.characters:
                if future_character.name == character.name:
                    #print("character match")
                    distanceBetweenVersions = character.getDistanceToFutureState(future_character.getAttributes())
                    distance += distanceBetweenVersions

    if len(currWorldState.characters) != len(newWorldState.characters):
        deadCharacterPenalty = abs(len(currWorldState.characters)-len(newWorldState.characters)) * 50 # Change this value to change weight of undesired deaths.
        distance += deadCharacterPenalty

    if newWorldState.drama_score != None:
        drama_distance = abs(currWorldState.drama_score - newWorldState.drama_score) * 5/2
        distance += drama_distance

    return distance
