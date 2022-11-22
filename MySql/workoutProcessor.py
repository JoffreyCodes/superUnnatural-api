import csv
'''
Processes WORKOUT_RAW.csv into 7 separate CSVs
1. WORKOUTS.csv
2. CLASSIC_WORKOUTS.csv
3. BOXING_WORKOUTS.csv
4. MEDITATION_WORKOUTS.csv
5. STRETCHING_WORKOUTS.csv
6. GENRE_LIST.csv
7. SONG_MAP_LIST.csv
'''

workouts = []
classicWorkouts = []
boxingWorkouts = []
meditationWorkouts = []
stretchingWorkouts = []
genreList = []
songMapList = []

PATH = "./Datasets/Processed/"


def createWorkouts(WorkoutId, Name, Description, Length, Date, WorkoutType, SpotifyUrl, CoachId, IntensityId):
    workout = [WorkoutId, Name, Description, Length, Date,
               WorkoutType, SpotifyUrl, CoachId, IntensityId]
    workouts.append(workout)


def createClassicWorkout(WorkoutId, MaxTargets, MaxTriangles, MaxKneeStrikes, MaxScore):
    if not MaxKneeStrikes:
        MaxKneeStrikes = 0
    workout = [WorkoutId, MaxTargets, MaxTriangles, MaxKneeStrikes, MaxScore]
    classicWorkouts.append(workout)


def createBoxingWorkout(WorkoutId, MaxTargets, MaxDodges, MaxKneeStrikes, MaxScore):
    if not MaxKneeStrikes:
        MaxKneeStrikes = 0
    workout = [WorkoutId, MaxTargets, MaxDodges, MaxKneeStrikes, MaxScore]
    boxingWorkouts.append(workout)


def createStretchingWorkout(WorkoutId):
    stretchingWorkouts.append([WorkoutId])


def createMeditationWorkout(WorkoutId):
    meditationWorkouts.append([WorkoutId])


def handleGenreList(WorkoutId, GenreIdListStr):
    if(GenreIdListStr == ''):
        createGenreList(WorkoutId, '')
    GenreIdList = GenreIdListStr.split(',')
    for i in range(len(GenreIdList)):
        createGenreList(WorkoutId, GenreIdList[i])


def createGenreList(WorkoutId, GenreId):
    if(GenreId):
        genreList.append([WorkoutId, GenreId])
    else:
        genreList.append([WorkoutId])


def handleSongMapLocationList(WorkoutId, SongIdListStr, LocationIdListStr):
    if SongIdListStr == '' or LocationIdListStr == '':
        return
    songIdList = SongIdListStr.split(',')
    locationIdList = LocationIdListStr.split(',')
    # determine minimun len of each row (some numSongs != numLocs)
    lenSongIdList = len(songIdList)
    lenLocationIdList = len(locationIdList)
    minLen = min(lenSongIdList, lenLocationIdList)
    # flatten each row and append to new list
    for i in range(minLen):
        songMapList.append([WorkoutId, songIdList[i], locationIdList[i]])


def createWorkoutsCSV():
    with open(PATH + "WORKOUTS.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(workouts)


def createClassicWorkoutsCSV():
    with open(PATH + "CLASSIC_WORKOUTS.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["WorkoutId", "MaxTargets", "MaxTriangles", "MaxScore"])
        writer.writerows(classicWorkouts)


def createBoxingWorkoutsCSV():
    with open(PATH + "BOXING_WORKOUTS.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["WorkoutId", "MaxTargets",
                         "MaxDodges", "MaxKneeStrikes", "MaxScore"])
        writer.writerows(boxingWorkouts)


def createMeditationWorkoutsCSV():
    with open(PATH + "MEDITATION_WORKOUTS.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["WorkoutId"])
        writer.writerows(meditationWorkouts)


def createStretchingWorkoutsCSV():
    with open(PATH + "STRETCHING_WORKOUTS.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["WorkoutId"])
        writer.writerows(stretchingWorkouts)


def createGenreListCSV():
    with open(PATH + "GENRE_LIST.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(genreList)


def createSongMapListCSV():
    with open(PATH + "SONG_MAP_LIST.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(songMapList)


with open('./Datasets/WORKOUTS_RAWDATA_11_22_2022.csv', mode='r', encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    maxLenDescription = 0
    for row in csv_reader:
        Name = row[0]
        Description = row[1]
        Date = row[2]
        IntensityId = row[3]
        Length = row[4]
        CoachId = row[5]
        GenreIdListStr = row[6]
        SongIdListStr = row[7]
        SpotifyUrl = row[8]
        WorkoutId = row[9]
        MaxTargets = row[10]
        LocationIdListStr = row[11]
        WorkoutType = row[12]
        MaxScore = row[13]
        MaxDodges = row[14]
        MaxKneeStrikes = row[15]
        MaxTriangles = row[16]
        maxLenDescription = max(maxLenDescription, len(Description))
        createWorkouts(WorkoutId, Name, Description, Length, Date,
                       WorkoutType, SpotifyUrl, CoachId, IntensityId)
        handleSongMapLocationList(WorkoutId, SongIdListStr, LocationIdListStr)
        handleGenreList(WorkoutId, GenreIdListStr)
        if(WorkoutType == 'classic'):
            createClassicWorkout(WorkoutId, MaxTargets,
                                 MaxTriangles, MaxKneeStrikes, MaxScore)
        if(WorkoutType == 'boxing'):
            createBoxingWorkout(WorkoutId, MaxTargets,
                                MaxDodges, MaxKneeStrikes, MaxScore)
        if(WorkoutType == 'meditation'):
            createMeditationWorkout(WorkoutId)
        if(WorkoutType == 'stretch'):
            createStretchingWorkout(WorkoutId)
print("maxCharDescription: " + str(maxLenDescription))
createWorkoutsCSV()
createClassicWorkoutsCSV()
createBoxingWorkoutsCSV()
createMeditationWorkoutsCSV()
createStretchingWorkoutsCSV()
createGenreListCSV()
createSongMapListCSV()
