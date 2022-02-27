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


if __name__ == "__main__":
    # Environment Initialization
    serenity = Environment("Serenity", 25, False, True)
    space = Environment("Space", -100, True, False)
    serenity.setDistance(space, 0)
    space.setDistance(serenity, 0)

    # Character & Relationship Initialization
    jess = Character("Jess", 10, 0, serenity)
    mal = Character("Mal", 10, 0, serenity)
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


