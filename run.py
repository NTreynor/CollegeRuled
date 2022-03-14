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
    #print("Runnable events found: ")
    #print(len(runableEvents))
    return runableEvents


def runStory(current_worldstate, possible_events, depth_limit, waypoints = None):
    if (depth_limit == 0):
        return current_worldstate
    
    runable_events = getRunableEvents(current_worldstate, possible_events)
    if len(runable_events) == 0:
        print("THE END")
        return current_worldstate

    # Setup to get story to pathfind to the first waypoint.
    if (waypoints != None) & (len(waypoints) != 0):
        #print("Waypoint found")
        desired_world_state = waypoints[0]
    else:
        print("No waypoint")
        desired_world_state = copy.deepcopy(current_worldstate) # TODO: Replace this with an actual goal worldstate

    #idx_of_event_to_run = selectEventIndex(runable_events, desired_world_state)[0]
    depthToSearch = min(depth_limit, 2)
    indexValuePair = getBestIndexLookingAhead(depthToSearch, runable_events, desired_world_state, possible_events) #First parameter indicates search depth. Do not exceed 6.
    idx_of_event_to_run = indexValuePair[0]
    #print("Event selected. Supposed distance: ")
    #print(indexValuePair[1])
    #print("Actual Distance: ")

    event = runable_events[idx_of_event_to_run][0]
    worldstate_to_run = runable_events[idx_of_event_to_run][1]
    chars_to_use = runable_events[idx_of_event_to_run][2]
    environments_to_use = runable_events[idx_of_event_to_run][3]
    next_worldstate = event.doEvent(worldstate_to_run, chars_to_use, environments_to_use)

    #print(distanceBetweenWorldstates(next_worldstate, waypoint))

    if desired_world_state.radius == None:
        desired_world_state.radius = 0
    if (distanceBetweenWorldstates(next_worldstate, desired_world_state) < desired_world_state.radius):
        #print(distanceBetweenWorldstates(next_worldstate, desired_world_state))
        print(". . .")
        #print(desired_world_state.radius)
        #print("Waypoint reached. Moving to next waypoint.")
        waypoints.pop(0)


    #print(distanceBetweenWorldstates(next_worldstate, desired_world_state))
    return runStory(next_worldstate, possible_events, depth_limit - 1, waypoints)

def waypointTestEnvironment():
    # Environment Initialization
    wp_serenity = Environment("Serenity", 25, False, True)
    wp_space = Environment("Space", -100, True, False)
    wp_serenity.setDistance(wp_space, 0)
    wp_space.setDistance(wp_serenity, 0)

    # Character & Relationship Initialization
    wp_jess = Character("Jess", health=8, happiness=8, location=wp_serenity, romantic_partner=False)
    wp_mal = Character("Mal", health=8, happiness=7, location=wp_serenity, romantic_partner=False)
    wp_inara = Character("Inara", health=8, happiness=5, location=wp_serenity, romantic_partner=False)

    wp_jess.updateRelationship(wp_mal, 45)
    wp_jess.updateRelationship(wp_inara, 0)
    wp_mal.updateRelationship(wp_jess, 45)
    wp_mal.updateRelationship(wp_inara, 35)
    wp_inara.updateRelationship(wp_jess, -5)
    wp_inara.updateRelationship(wp_mal, 35)

    wp_environments = [wp_serenity, wp_space]
    wp_chars = [wp_jess, wp_mal, wp_inara]
    wp_curr_worldstate = WorldState(0, wp_chars, wp_environments)

    wp_init_worldstate = copy.deepcopy(wp_curr_worldstate) # Save FIRST worldstate

    # Update characters for second waypoint
    wp_jess.health = None
    wp_mal.health = None
    wp_inara.health = None
    wp_jess.happiness = None
    wp_mal.happiness = None
    wp_inara.happiness = None
    wp_jess.updateRelationship(wp_mal, 30)
    wp_mal.updateRelationship(wp_jess, 40)
    wp_jess.romantic_partner = wp_mal
    wp_mal.romantic_partner = wp_jess
    wp_chars = [wp_jess, wp_mal, wp_inara]

    wp_curr_worldstate = WorldState(0, wp_chars, wp_environments, 10)
    wp_2_worldstate = copy.deepcopy(wp_curr_worldstate) # Save second waypoint
    wp_2_worldstate.drama_score = 15


    wp_jess.updateRelationship(wp_mal, -30)
    wp_mal.updateRelationship(wp_jess, -30)
    wp_mal.updateRelationship(wp_inara, 30)
    wp_inara.updateRelationship(wp_mal, 45)
    wp_mal.romantic_partner = wp_inara
    wp_chars = [wp_mal, wp_inara]


    wp_curr_worldstate = WorldState(0, wp_chars, wp_environments, 5)
    wp_3_worldstate = copy.deepcopy(wp_curr_worldstate) # Save third waypoint
    wp_inara.murderer = True
    wp_3_worldstate.drama_score = 1000

    waypoints = [wp_2_worldstate, wp_3_worldstate]
    starting_point = wp_init_worldstate

    return [starting_point, waypoints]

if __name__ == "__main__":
    # Environment Initialization
    serenity = Environment("Serenity", 25, False, True)
    space = Environment("Space", -100, True, False)
    serenity.setDistance(space, 0)
    space.setDistance(serenity, 0)

    # Character & Relationship Initialization
    jess = Character("Jess", health=7, happiness=10, location=serenity)
    mal = Character("Mal", health=7, happiness=10, location=serenity)
    inara = Character("Inara", health=10, happiness=0, location=serenity)

    jess.updateRelationship(mal, 45)
    mal.updateRelationship(jess, 45)
    inara.updateRelationship(jess, 45)
    inara.updateRelationship(mal, 45)

    happy_jess = Character("Jess", happiness=10, location=serenity)
    happy_mal = Character("Mal", happiness=10, location=serenity)
    heartbroken_inara = Character("Inara", location=serenity)

    happy_jess.updateRelationship(happy_mal, 90)
    happy_mal.updateRelationship(happy_jess, 70)

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
                        HospitalVisit(), Cheat(), Steal(), Irritate(), Befriend(), LoseJob(),
                        AssistedJailBreak(), SabotagedJailBreak(), DoNothing()]

    loveEvents = [FallInLove(), AskOnDate(), Cheat(), Irritate(), Befriend()]
    #loveEvents = [FallInLove(), Cheat()]
    simpleTest = [FallInLove(), AskOnDate(), DoNothing()]

    #runStory(initialState, loveEvents, 5, updateState)
    #runStory(initialState, simpleTest, 5, updateState)
    #print(distanceBetweenWorldstates(initialState, updateState))

    """
    #"TALE OF WOE AND MISERY:"
    finalState = runStory(initialState, possibleEvents, 25, updateState)

    print("Starting Distance: ")
    print(distanceBetweenWorldstates(initialState, updateState))

    print("Final Distance: ")
    print(distanceBetweenWorldstates(finalState, updateState))

    
    finalState = runStory(initialState, simpleTest, 10, loveState)

    print("Starting Distance: ")
    print(distanceBetweenWorldstates(initialState, loveState))

    print("Final Distance: ")
    print(distanceBetweenWorldstates(finalState, loveState))
    """
   #for character in finalState.characters:
    #    print(character)
    #    print (character.relationships)

    initWorldState, waypoints = waypointTestEnvironment()
    runStory(initWorldState, possibleEvents, 15, waypoints)





