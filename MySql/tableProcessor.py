import csv
import json
'''
Processes airtable csv with focus on the Workouts view.
Source Data: https://airtable.com/shrcuUWyR76gcdbqw/tblMuteBHqIjaYplx/viwLtKByxy8UB2JG2 
Location table is handled separately.
The INPUT_WORKOUTS_FILE csv expects the following columns:
    Name                    Description                 Date
    Name (from Intensity)   SN ID (from Intensity)      Chew Rating
    Length                  Name (from Coach)           SN ID (from Coach)
    Name (from Genre)       SN ID (from Genre)          Song Name (from Songs)
    Artist (from Songs)     Length (from Songs)         SN ID (from Songs)
    Spotify Link            SN ID                       Triangles
    Max Targets             Max Score                   Points Per Minute
    Targets Per Minute      Workout Type                Max Dodges
    Max Knee Strikes        SN ID (from Locations)
'''

INPUT_WORKOUTS_FILE = './Datasets/WORKOUTS_FLATTENED_11_29_2022.csv'
INPUT_LOCATIONS_FILE = './Datasets/LOCATIONS_FLATTENED_11_29_2022.csv'
PATH = "./Datasets/ProcessedFiles/"
PROCESS_JSON = True
PROCESS_CSV = False

def main():
    runProcessor()
    for table in createInstrxn.keys():
        if(PROCESS_JSON): createJSON(createInstrxn[table]['filename'], createInstrxn[table]['items'])
        if(PROCESS_CSV): createCSV(createInstrxn[table]['filename'], createInstrxn[table]['headers'], createInstrxn[table]['items'])


def runLocationsProcessor():
    with open(INPUT_LOCATIONS_FILE, mode='r', encoding="utf-8-sig") as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        next(reader, None)
        for row in reader:
            locationEntry = {}
            for i in range(len(row)):
                colNames = createInstrxn['locations']['headers']
                locationEntry[colNames[i]] = row[i]
            createInstrxn['locations']['items'].append(locationEntry)

def getHeaders():
    headers = {}
    with open(INPUT_WORKOUTS_FILE, mode='r', encoding="utf-8-sig") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            for col in range(len(row)):
                colName = row[col]
                headers[colName] = col
            break
    return headers

def get(val):
    headers = getHeaders()
    return headers.get(val)

def runProcessor():
    # process locations using locations data file
    runLocationsProcessor()
    with open(INPUT_WORKOUTS_FILE, mode='r', encoding="utf-8-sig") as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        # skip header row
        next(reader, None)
        for row in reader:
            processWorkoutType(row)
            processTable(row,'songs')
            processTable(row,'coaches')
            processTable(row,'genres')
            processTable(row,'intensities')
            handleGenreList(row, 'genrelist')
            handleSongMapLocationList(row, 'songmaps')

def handleGenreList(row, table):
    WorkoutId = row[get('SN ID')]
    GenreIdListStr = row[get('SN ID (from Genre)')]
    if(GenreIdListStr == ''):
        createGenreList(WorkoutId, table, '')
    GenreIdList = [id.strip() for id in GenreIdListStr.split(',')]
    for i in range(len(GenreIdList)):
        createGenreList(WorkoutId, table, GenreIdList[i])


def createGenreList(WorkoutId, table, GenreId):
    genreList = createInstrxn[table]['items']
    if(GenreId):
        genreList.append({'SN ID':WorkoutId, 'SN ID (from Genre)' : GenreId})
    else:
        genreList.append({'SN ID':WorkoutId})


def handleSongMapLocationList(row, table):
    WorkoutId = row[get('SN ID')]
    SongIdListStr = row[get('SN ID (from Songs)')]
    LocationIdListStr = row[get('SN ID (from Locations)')]
    songMapList = createInstrxn[table]['items']
    if SongIdListStr == '' or LocationIdListStr == '':
        return
    songIdList = [id.strip() for id in SongIdListStr.split(',')]
    locationIdList = [id.strip() for id in LocationIdListStr.split(',')]
    # determine minimun len of each row (some numSongs != numLocs)
    lenSongIdList = len(songIdList)
    lenLocationIdList = len(locationIdList)
    minLen = min(lenSongIdList, lenLocationIdList)
    # flatten each row and append to new list
    for i in range(minLen):
        songMapList.append({
            'SN ID':WorkoutId, 
            'SN ID (from Songs)': songIdList[i], 
            'SN ID (from Locations)':locationIdList[i]
        })

def processTable(row, table):
    # if no elems, skip
    tablePk = createInstrxn[table]['primary_key']
    colTablePk = row[get(tablePk)]    
    if colTablePk == '' : return
    
    # handle multiple elems in a row
    tablePkList = [int(pk) for pk in colTablePk.split(',')]
    numElems = len(tablePkList)
    for i in range(numElems):
        # skip if already encountered (from prev rows)
        pk = tablePkList[i]
        pkSet = createInstrxn[table]['pk_set']
        if pk in pkSet: continue
        
        # create entry, add elems to list (via headers), add pk to set  
        tableElem = {}
        headers = createInstrxn[table]['headers']
        for header in headers:
            tableElem[header] = [item.strip() for item in row[get(header)].split(',')][i]
        tableList = createInstrxn[table]['items']
        tableList.append(tableElem) 
        pkSet.add(pk)

def processWorkoutType(row):
    # process all rows as a workout
    processRow(row, createInstrxn['workouts']['items'], createInstrxn['workouts']['headers'])
    # process subcategorical workouts by type
    workoutType = row[get('Workout Type')]
    workoutTypes = ['classic', 'boxing', 'meditation', 'stretch']
    for type in workoutTypes:
        if workoutType == type:
            processRow(row, createInstrxn[type]['items'], createInstrxn[type]['headers'])

def processRow(row, list, headers):
    entry = {}
    for header in headers:
        entry[header] = row[get(header)] if row[get(header)] != '' else 0
    list.append(entry)

def createCSV(filename, headers, items):
    with open(PATH + 'CSV/' + filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        writer.writerows(items)

def createJSON(filename, items):
    with open(PATH + 'JSON/' + filename + '.json', "w") as out:
        json.dump(items, out, indent=2)

createInstrxn = {
    'workouts': {
        'items' : [],
        'headers' : [
            'SN ID', 'Name', 'Description', 'Length', 
            'Date', 'Workout Type', 'Spotify Link', 
            'SN ID (from Coach)', 'SN ID (from Intensity)' ],
        'primary_key': 'SN ID',
        'filename' : 'WORKOUTS'
    },
    'classic': {
        'items' : [],
        'headers' : [
            'SN ID', 'Max Targets', 'Triangles',
            'Max Knee Strikes', 'Max Score', 
            'Points Per Minute', 'Targets Per Minute' ],
        'primary_key': 'SN ID', 
        'filename' : 'CLASSIC_WORKOUTS'
    },
    'boxing': {
        'items' : [],
        'headers' : [
            'SN ID', 'Max Targets', 'Max Dodges',
            'Max Knee Strikes', 'Max Score', 
            'Points Per Minute', 'Targets Per Minute' ],
        'primary_key': 'SN ID', 
        'filename' : 'BOXING_WORKOUTS'
    },
    'meditation': {
        'items' : [],
        'headers' : ['SN ID'],
        'primary_key': 'SN ID', 
        'filename' : 'MEDITATION_WORKOUTS'
    },
    'stretch': {
        'items' : [],
        'headers' : ['SN ID'],   
        'primary_key': 'SN ID', 
        'filename' : 'STRETCH_WORKOUTS'
    },
    'songs': {
        'pk_set': set(),
        'items' : [],
        'headers' : [
            'SN ID (from Songs)','Song Name (from Songs)',
            'Artist (from Songs)', 'Length (from Songs)' ], 
        'primary_key': 'SN ID (from Songs)',
        'filename' : 'SONGS'
    },
    'coaches': {
        'pk_set': set(),
        'items' : [],
        'headers' : [
            'SN ID (from Coach)',
            'Name (from Coach)'], 
        'primary_key': 'SN ID (from Coach)',
        'filename' : 'COACHES'
    },
    'genres': {
        'pk_set': set(),
        'items' : [],
        'headers' : [
            'SN ID (from Genre)',
            'Name (from Genre)'], 
        'primary_key': 'SN ID (from Genre)',
        'filename' : 'GENRES'
    },
    'intensities': {
        'pk_set': set(),
        'items' : [],
        'headers' : [
            'SN ID (from Intensity)',
            'Name (from Intensity)'], 
        'primary_key': 'SN ID (from Intensity)',
        'filename' : 'INTENSITIES'
    },
    'locations': {
        'items' : [],
        'headers' : [
            'Name', 'Screenshot',
            'SN ID', 'Near the Ground'], 
        'filename' : 'LOCATIONS'
    },
    'songmaps': {
        'items' : [],
        'headers' : [
            'SN ID', 'SN ID (from Songs)',
            'SN ID (from Locations)'], 
        'filename' : 'SONGMAPSLIST'
    },
    'genrelist': {
        'items' : [],
        'headers' : [
            'SN ID', 'SN ID (from Genre)'], 
        'filename' : 'GENRELIST'
    }
}

main()