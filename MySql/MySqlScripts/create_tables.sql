CREATE SCHEMA IF NOT EXISTS supernatural_cms;
USE supernatural_cms;

DROP TABLE IF EXISTS SongMaps;
DROP TABLE IF EXISTS Songs;
DROP TABLE IF EXISTS Locations;
DROP TABLE IF EXISTS GenreList;
DROP TABLE IF EXISTS Genres;
DROP TABLE IF EXISTS Classic;
DROP TABLE IF EXISTS Boxing;
DROP TABLE IF EXISTS Meditation;
DROP TABLE IF EXISTS Stretch;
DROP TABLE IF EXISTS Workouts;
DROP TABLE IF EXISTS Intensities;
DROP TABLE IF EXISTS Coaches; 

CREATE TABLE Coaches (
	CoachId INT,
    Name VARCHAR(255),
	CONSTRAINT pk_Coaches_CoachId PRIMARY KEY (CoachId)
);

CREATE TABLE Intensities (	
	IntensityId INT,
    Name VARCHAR(255),
	CONSTRAINT pk_Intensities_IntensityId PRIMARY KEY (IntensityId)
);

CREATE TABLE Workouts (
	WorkoutId INT,
    Name VARCHAR(255),
    Description VARCHAR(325),
    Duration TIME,
    Date VARCHAR(255),
    WorkoutType VARCHAR(255),
    SpotifyUrl VARCHAR(255),
    CoachId INT,
    IntensityId INT,
    CONSTRAINT pk_Workouts_WorkoutId PRIMARY KEY (WorkoutId),
    CONSTRAINT fk_Workouts_CoachId FOREIGN KEY (CoachId)
		REFERENCES Coaches(CoachId)
		ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_Workouts_IntensityId FOREIGN KEY (IntensityId)
		REFERENCES Intensities(IntensityId)
		ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE Classic (
WorkoutId INT,
MaxTargets INT,
MaxTriangles INT,
MaxKneeStrikes INT,
MaxScore INT,
CONSTRAINT pk_Classic_WorkoutId PRIMARY KEY (WorkoutId),
CONSTRAINT fk_Classic_WorkoutId FOREIGN KEY (WorkoutId)
	REFERENCES Workouts(WorkoutId)
    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Boxing (
WorkoutId INT,
MaxTargets INT,
MaxDodges INT,
MaxKneeStrikes INT,
MaxScore INT,
CONSTRAINT pk_Boxing_WorkoutId PRIMARY KEY (WorkoutId),
CONSTRAINT fk_Boxing_WorkoutId FOREIGN KEY (WorkoutId)
	REFERENCES Workouts(WorkoutId)
    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Meditation (
WorkoutId INT,
CONSTRAINT pk_Meditation_WorkoutId PRIMARY KEY (WorkoutId),
CONSTRAINT fk_Meditation_WorkoutId FOREIGN KEY (WorkoutId)
	REFERENCES Workouts(WorkoutId)
    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Stretch (
WorkoutId INT,
CONSTRAINT pk_Stretch_WorkoutId PRIMARY KEY (WorkoutId),
CONSTRAINT fk_Stretch_WorkoutId FOREIGN KEY (WorkoutId)
	REFERENCES Workouts(WorkoutId)
    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Genres (	
	GenreId INT,
    Name VARCHAR(255),
	CONSTRAINT pk_Genres_GenreId PRIMARY KEY (GenreId)
);

CREATE TABLE GenreList (	
	GenreListId INT AUTO_INCREMENT,
    WorkoutId INT,
    GenreId INT,
	CONSTRAINT pk_GenreList_GenreListId PRIMARY KEY (GenreListId),
    CONSTRAINT fk_GenreList_WorkoutId FOREIGN KEY (WorkoutId)
		REFERENCES Workouts(WorkoutId)
		ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_GenreList_GenreId FOREIGN KEY (GenreId)
		REFERENCES Genres(GenreId)
		ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Songs (	
	SongId INT,
    Name VARCHAR(255),
    Artist VARCHAR(255),
    Length VARCHAR(255),
	CONSTRAINT pk_Songs_SongId PRIMARY KEY (SongId)
);

CREATE TABLE Locations (
	LocationId INT,
	Name VARCHAR(255),
    ScreenshotUrl VARCHAR(255),
    NearGround BOOL,
	CONSTRAINT pk_Locations_LocationId PRIMARY KEY (LocationId)
);

CREATE TABLE SongMaps (	
	SongMapId INT AUTO_INCREMENT,
    WorkoutId INT,
    SongId INT,
    LocationId INT,
	CONSTRAINT pk_SongMaps_SongMapId PRIMARY KEY (SongMapId),
	CONSTRAINT fk_SongMaps_WorkoutId FOREIGN KEY (WorkoutId)
		REFERENCES Workouts(WorkoutId)
		ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT fk_SongMaps_SongId FOREIGN KEY (SongId)
		REFERENCES Songs(SongId)
		ON UPDATE CASCADE ON DELETE SET NULL,
	CONSTRAINT fk_SongMaps_LocationId FOREIGN KEY (LocationId)
		REFERENCES Locations(LocationId)
		ON UPDATE CASCADE ON DELETE SET NULL
);