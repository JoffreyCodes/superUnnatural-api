CREATE SCHEMA IF NOT EXISTS superunnatural;
USE superunnatural;

DROP TABLE IF EXISTS Notes;

CREATE TABLE Notes (
	NoteId INT AUTO_INCREMENT,
    SpUserId INT,
    SnWorkoutId INT,
    SnTrackId INT,
	Content VARCHAR(255),
	Created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT pk_Notes_NotedId PRIMARY KEY (NoteId)
);
