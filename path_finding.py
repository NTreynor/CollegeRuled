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
        #print("x = " + str(x))
        currEventValue = distanceBetweenWorldstates(desiredWorldState, eventList[x][0].getNewWorldstate(eventList[x][1], eventList[x][2], eventList[x][3]))
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
    for character in currWorldState.characters:
        for future_character in newWorldState.characters:
            if future_character.name == character.name:
                distance += character.getDistanceToFutureState(future_character.getAttributes())
    # TODO: do something more interesting with drama distance
    drama_distance = abs(currWorldState.drama_score ** 2 - newWorldState.drama_score**2)**(1/2)
    print("Distance between world states is {}".format(distance))
    #return 5
    return distance
