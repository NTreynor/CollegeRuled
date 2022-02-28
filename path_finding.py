from backbone_classes import *
from events import *
import random

def selectEventIndex(eventList, desiredWorldState):
    #print("attempting to select event index")
    currMinDistanceEventIndex = -1
    currEventMinDistance = 9999
    equallyValubleIndexes = []
    #print(len(eventList))
    for x in range (len(eventList)):

        #print("Index in list of events checked:")
        #print(x)
        #print("x = " + str(x))
        reachable_worldstate = eventList[x][0].getNewWorldState(eventList[x][1], eventList[x][2], eventList[x][3])
        currEventValue = distanceBetweenWorldstates(desiredWorldState, reachable_worldstate)
        if (currEventValue < currEventMinDistance):
            equallyValubleIndexes = []
            currEventMinDistance = currEventValue
            currMinDistanceEventIndex = x
            equallyValubleIndexes.append(x)
        if (currEventValue == currEventMinDistance):
            equallyValubleIndexes.append(x)

    return random.choice(equallyValubleIndexes) # Return the index of the event with the lowest distance to the desiredWorldState


def distanceBetweenWorldstates(currWorldState, newWorldState):
    distance = 0
    if currWorldState.characters:
        for character in currWorldState.characters:
            for future_character in newWorldState.characters:
                if future_character.name == character.name:
                    distance += character.getDistanceToFutureState(future_character.getAttributes())
    drama_distance = abs(currWorldState.drama_score - newWorldState.drama_score) * 5/2
    distance += drama_distance
    print("Distance between world states is {}".format(distance))
    #return distance
    return 5 #outputting a fixed distance causes the system to default to random event selection.
