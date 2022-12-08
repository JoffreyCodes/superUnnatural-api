import json
import datetime

from models.genre import Genre, GenreList
from models.coach import Coach
from models.intensity import Intensity
from models.songLocations import Song, Location, SongLocation
from models.workout import Workout, Stretch, Meditation, Boxing, Classic
from database import db, engine, base

PATH = "../MySql/Datasets/ProcessedFiles/JSON/"
GENRES_PATH = PATH + "GENRES.json"
COACHES_PATH = PATH + "COACHES.json"
INTENSITIES_PATH = PATH + "INTENSITIES.json"
LOCATIONS_PATH = PATH + "LOCATIONS.json"
SONGS_PATH = PATH + "SONGS.json"
WORKOUTS_PATH = PATH + "WORKOUTS.json"
MEDITATION_WORKOUTS_PATH = PATH + "MEDITATION_WORKOUTS.json"
STRETCH_WORKOUTS_PATH = PATH + "STRETCH_WORKOUTS.json"
BOXING_WORKOUTS_PATH = PATH + "BOXING_WORKOUTS.json"
CLASSIC_WORKOUTS_PATH = PATH + "CLASSIC_WORKOUTS.json"
SONGLOCATIONSLIST_PATH = PATH + "SONGLOCATIONSLIST.json"
GENRELIST_PATH = PATH + "GENRELIST.json"

def getAttrs(classObj):
    return [k for k in classObj.__dict__.keys()
                if not k.startswith('_')
                and not k.endswith('_')]

def dropTable(table_name):
    metadata = db.Model.metadata
    table = metadata.tables.get(table_name)
    if table is not None:
        base.metadata.drop_all(engine, [table], checkfirst=True)

def dropAll():
    dropTable(GenreList.__tablename__)
    dropTable(SongLocation.__tablename__)
    dropTable(Boxing.__tablename__)
    dropTable(Classic.__tablename__)
    dropTable(Meditation.__tablename__)
    dropTable(Stretch.__tablename__)
    dropTable(Workout.__tablename__)
    dropTable(Song.__tablename__)
    dropTable(Location.__tablename__)
    dropTable(Intensity.__tablename__)
    dropTable(Coach.__tablename__)
    dropTable(Genre.__tablename__)


def loadDb():
    dropAll()
    db.create_all()
    loadFiles(GENRES_PATH, Genre)
    loadFiles(COACHES_PATH, Coach)
    loadFiles(INTENSITIES_PATH, Intensity)
    loadFiles(LOCATIONS_PATH, Location)
    loadFiles(SONGS_PATH, Song)
    loadWorkouts(WORKOUTS_PATH)
    db.session.commit()
    
    loadFiles(SONGLOCATIONSLIST_PATH, SongLocation)
    loadFiles(GENRELIST_PATH, GenreList)
    db.session.commit()

def loadFiles(file, classObj):
    data = json.load(open(file, 'r'))
    for entry in data:
        # get entry data as values
        vals = [entry[key] for key in entry.keys()]
        # get named attrs as keys
        classAttrs = getAttrs(classObj)
        # kv pair as dict
        params = dict(zip(classAttrs, vals))
        #  ** to indicate named params from kv pairs
        obj = classObj(**params)
        db.session.add(obj)


def loadWorkouts(file):
    data = json.load(open(file, 'r'))
    for workout in data:
        workoutDict = getWorkoutParamsDict(workout)
        workoutEntry = None
        if workout['Workout Type'] == 'meditation':  
            workoutEntry = Meditation(**workoutDict)
        elif workout['Workout Type'] == 'stretch':  
            workoutEntry = Stretch(**workoutDict)
        elif workout['Workout Type'] == 'boxing':  
            boxingDict = getBoxingParamsDict(workout)
            workoutDict.update(boxingDict)
            workoutEntry = Boxing(**workoutDict)
        elif workout['Workout Type'] == 'classic':  
            classicDict = getClassicParamsDict(workout)
            workoutDict.update(classicDict)
            workoutEntry = Classic(**workoutDict)
        else: 
            workoutEntry = Workout(**workoutDict)
        db.session.add(workoutEntry)

def getWorkoutParamsDict(workout):
    workoutDict = {}
    workoutDict['WorkoutId'] = workout['SN ID']
    workoutDict['Name'] = workout['Name']
    workoutDict['Description'] = workout['Description']
    workoutDict['Length'] = getSec(workout['Length'] )
    workoutDict['Date'] = getDatetime( workout['Date'])
    workoutDict['WorkoutType'] = workout['Workout Type']
    workoutDict['SpotifyUrl'] = workout['Spotify Link']
    workoutDict['CoachId'] = workout['SN ID (from Coach)']
    workoutDict['IntensityId'] = workout['SN ID (from Intensity)']
    return workoutDict

def getBoxingParamsDict(workout):
    boxingDict = {}
    boxingDict['WorkoutId'] = workout["SN ID"]
    boxingDict['MaxTargets'] = workout["Max Targets"]
    boxingDict['MaxDodges'] = workout["Max Dodges"]
    boxingDict['MaxKneeStrikes'] = workout["Max Knee Strikes"]
    boxingDict['MaxScore'] = workout["Max Score"]
    boxingDict['PointsPerMin'] = workout["Points Per Minute"]
    boxingDict['TargetsPerMin'] = workout["Targets Per Minute"]
    return boxingDict

def getClassicParamsDict(workout):
    classicDict = {}
    classicDict['WorkoutId'] = workout['SN ID']
    classicDict['MaxTargets'] = workout['Max Targets']
    classicDict['Triangles'] = workout['Triangles']
    classicDict['MaxKneeStrikes'] = workout['Max Knee Strikes']
    classicDict['MaxScore'] = workout['Max Score']
    classicDict['PointsPerMin'] = workout['Points Per Minute']
    classicDict['TargetsPerMin'] = workout['Targets Per Minute']
    return classicDict

"""Get seconds from time."""
def getSec(time_str):    
    hasHours = len(time_str.split(':')) == 3
    if hasHours:
        h, m, s = time_str.split(':')
        return int(h) * 3600 + int(m) * 60 + int(s) * 60
    else:    
        m, s = time_str.split(':')
        return int(m) * 60 + int(s) * 60

"""Gets datetime from mm/dd/yyyy"""
def getDatetime(date_str):
    month, day, year = [int(x) for x in date_str.split('/')]
    return datetime.date(year,month,day)