import csv
'''
Processes airtable csv with focus on the Workouts view. 
Location table is handled separately.
The read-in csv expects the following columns:
    Name                    Description                 Date
    Name (from Intensity)   SN ID (from Intensity)      Chew Rating
    Length                  Name (from Coach)           SN ID (from Coach)
    Name (from Genre)       SN ID (from Genre)          Song Name (from Songs)
    Artist (from Songs)     Length (from Songs)         SN ID (from Songs)
    Spotify Link            SN ID                       Triangles
    Max Targets             Screenshot (from Locations) Name (from Locations)
    SN ID (from Locations)  Near the Ground (from Locations)
    Max Score               Points Per Minute           Targets Per Minute
    Workout Type            Max Dodges                  Max Knee Strikes
'''
data = {
    'workouts': {
        'items' : [],
        'headers' : [
            'SN ID', 'Name', 'Description', 'Length', 
            'Date', 'Workout Type', 'Spotify Link', 
            'SN ID (from Coach)', 'SN ID (from Intensity)' ],
        'primary_key': 'SN ID',
        'filename' : 'WORKOUTS.csv'
    },
    'classic_workouts': {
        'items' : [],
        'headers' : [
            'SN ID', 'Max Targets', 'Triangles',
            'Max Knee Strikes', 'Max Score', 
            'Points Per Minute', 'Targets Per Minute' ],
        'primary_key': 'SN ID', 
        'filename' : 'CLASSIC_WORKOUTS.csv'
    },
    'boxing_workouts': {
        'items' : [],
        'headers' : [
            'SN ID', 'Max Targets', 'Max Dodges',
            'Max Knee Strikes', 'Max Score', 
            'Points Per Minute', 'Targets Per Minute' ],
        'primary_key': 'SN ID', 
        'filename' : 'BOXING_WORKOUTS.csv'
    },
    'meditation_workouts': {
        'items' : [],
        'headers' : ['SN ID'],
        'primary_key': 'SN ID', 
        'filename' : 'MEDITATION_WORKOUTS.csv'
    },
    'stretch_workouts': {
        'items' : [],
        'headers' : ['SN ID'],   
        'primary_key': 'SN ID', 
        'filename' : 'STRETCH_WORKOUTS.csv'
    },
    'songs': {
        'pk_set': set(),
        'items' : [],
        'headers' : [
            'SN ID (from Songs)','Song Name (from Songs)',
            'Artist (from Songs)', 'Length (from Songs)' ], 
        'primary_key': 'SN ID (from Songs)',
        'filename' : 'SONGS.csv'
    },
    'coaches': {
        'pk_set': set(),
        'items' : [],
        'headers' : [
            'SN ID (from Coach)',
            'Name (from Coach)'], 
        'primary_key': 'SN ID (from Coach)',
        'filename' : 'COACHES.csv'
    },
    'genres': {
        'pk_set': set(),
        'items' : [],
        'headers' : [
            'SN ID (from Genre)',
            'Name (from Genre)'], 
        'primary_key': 'SN ID (from Genre)',
        'filename' : 'GENRES.csv'
    },
    'intensities': {
        'pk_set': set(),
        'items' : [],
        'headers' : [
            'SN ID (from Intensity)',
            'Name (from Intensity)'], 
        'primary_key': 'SN ID (from Intensity)',
        'filename' : 'INTENSITIES.csv'
    },
}

PATH = "./Datasets/ProcessedFiles/"

def getHeaders():
    headers = {}
    with open('./Datasets/WORKOUTS_FLATTENED_11_29_2022.csv', mode='r', encoding="utf-8-sig") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            for col in range(len(row)):
                colName = row[col]
                headers[colName] = col
            break
    return headers

def get(val):
    return headers.get(val)

def runProcessor():
    with open('./Datasets/WORKOUTS_FLATTENED_11_29_2022.csv', mode='r', encoding="utf-8-sig") as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        next(reader, None)
        for row in reader:
            processWorkoutType(row)
            processTable(row,'songs')
            processTable(row,'coaches')
            processTable(row,'genres')
            processTable(row,'intensities')

def processTable(row, table):
    # if no elems, skip
    tablePk = data[table]['primary_key']
    colTablePk = row[get(tablePk)]    
    if colTablePk == '' : return
    
    # handle multiple elems in a row
    tablePkList = [int(pk) for pk in colTablePk.split(',')]
    numElems = len(tablePkList)
    for i in range(numElems):
        # skip if already encountered (from prev rows)
        pk = tablePkList[i]
        pkSet = data[table]['pk_set']
        if pk in pkSet: continue
        
        # create entry, add elems to list (via headers), add pk to set  
        tableElem = {}
        headers = data[table]['headers']
        for header in headers:
            tableElem[header] = [item.strip() for item in row[get(header)].split(',')][i]
        tableList = data[table]['items']
        tableList.append(tableElem) 
        pkSet.add(pk)

def processWorkoutType(row):
    processRow(row, data['workouts']['items'], data['workouts']['headers'])
    workoutType = row[get('Workout Type')]
    if(workoutType == 'classic'):
        processRow(row, data['classic_workouts']['items'], data['classic_workouts']['headers'])
    if(workoutType == 'boxing'):
        processRow(row, data['boxing_workouts']['items'], data['boxing_workouts']['headers'])
    if(workoutType == 'meditation'):
        processRow(row, data['meditation_workouts']['items'], data['meditation_workouts']['headers'])
    if(workoutType == 'stretch'):
        processRow(row, data['stretch_workouts']['items'], data['stretch_workouts']['headers'])

def processRow(row, list, headers):
    data = {}
    for header in headers:
        data[header] = row[get(header)] if row[get(header)] != '' else 0
    list.append(data)

def createCSV(filename, headers, items):
    with open(PATH + filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        writer.writerows(items)

headers = getHeaders()
runProcessor()
for table in data.keys():
    createCSV(data[table]['filename'], data[table]['headers'], data[table]['items'])