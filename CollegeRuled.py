from git.exc import GitCommandError
from pydriller import Repository
from pydriller.metrics.process.code_churn import CodeChurn
from pydriller.metrics.process.commits_count import CommitsCount
from datetime import datetime, timedelta, timezone
import pandas as pd
import pytz


class Character:
    def __init__(self, name, happiness):
        self.name = id
        self.happiness = happiness
        #self.location
        self.relationships = {}

    def updateRelationship(self, other_character, friendship_enemy_index):
        self.relationships[other_character] = friendship_enemy_index

    def __str__(self):
        return "Character name is %s. Relationship matrix is: %s." % (self.name, str(self.relationships))

class Environment:
    def __init__(self, name, quality):
        self.name = id
        self.quality = quality
        self.distances = {}

    def setDistance(self, other_environment, distance_index):
        self.distances[other_environment] = distance_index

    def __str__(self):
        return "Environment name is %s. Distance matrix is: %s." % (self.name, str(self.distances))

class WorldState:
    def __init__(self, date):
        self.date = date

    def __str__(self):
        return ""

def main():
    return 0
