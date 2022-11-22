USE supernatural_cms;

LOAD DATA INFILE '/ProgramData/MySQL/MySQL Server 5.7/etc/SupernaturalCMS/Datasets/Processed/COACHES.csv' 
	IGNORE INTO TABLE Coaches
	FIELDS TERMINATED BY ','
	ENCLOSED BY '"'
	# Windows platforms may need '\r\n'
	LINES TERMINATED BY '\r\n'
	IGNORE 1 LINES
	(@Name, @CoachId)
	SET Name=@Name, CoachId=@CoachId; 

LOAD DATA INFILE '/ProgramData/MySQL/MySQL Server 5.7/etc/SupernaturalCMS/Datasets/Processed/INTENSITIES.csv' 
	IGNORE INTO TABLE Intensities
	FIELDS TERMINATED BY ','
	ENCLOSED BY '"'
	LINES TERMINATED BY '\r\n'
	IGNORE 1 LINES
	(@Name, @IntensityId)
	SET IntensityId=@IntensityId, Name=@Name;

LOAD DATA INFILE '/ProgramData/MySQL/MySQL Server 5.7/etc/SupernaturalCMS/Datasets/Processed/WORKOUTS.csv' 
	IGNORE INTO TABLE Workouts
	FIELDS TERMINATED BY ','
	ENCLOSED BY '"'
	LINES TERMINATED BY '\r\n'
	IGNORE 1 LINES
	(@WorkoutId, @Name, @Description, @Length, @Date, @WorkoutType, @SpotifyUrl, @CoachId, @IntensityId)
	SET WorkoutId=@WorkoutId, Name=@Name, Description=@Description, Duration=@Length, Date=@Date, WorkoutType=@WorkoutType, SpotifyUrl=@SpotifyUrl, CoachId=@CoachId, IntensityId=@IntensityId;

LOAD DATA INFILE '/ProgramData/MySQL/MySQL Server 5.7/etc/SupernaturalCMS/Datasets/Processed/BOXING_WORKOUTS.csv' 
	IGNORE INTO TABLE Boxing
	FIELDS TERMINATED BY ','
	ENCLOSED BY '"'
	LINES TERMINATED BY '\r\n'
	IGNORE 1 LINES
	(@WorkoutId, @MaxTargets, @MaxDodges, @MaxKneeStrikes, @MaxScore)
    SET WorkoutId=@WorkoutId, 
    MaxTargets=@MaxTargets, 
    MaxDodges=CASE WHEN @MaxDodges = '' THEN 0 ELSE @MaxDodges END, 
    MaxKneeStrikes=@MaxKneeStrikes, 
    MaxScore=CASE WHEN @MaxScore  = '' THEN 0 ELSE @MaxScore END;

LOAD DATA INFILE '/ProgramData/MySQL/MySQL Server 5.7/etc/SupernaturalCMS/Datasets/Processed/CLASSIC_WORKOUTS.csv' 
	IGNORE INTO TABLE Classic
	FIELDS TERMINATED BY ','
	ENCLOSED BY '"'
	LINES TERMINATED BY '\r\n'
	IGNORE 1 LINES
	(@WorkoutId, @MaxTargets, @MaxTriangles, @MaxKneeStrikes, @MaxScore)
    SET WorkoutId=@WorkoutId, 
    MaxTargets= @MaxTargets, 
    MaxTriangles=@MaxTriangles, 
    MaxKneeStrikes=@MaxKneeStrikes, 
    MaxScore=CASE WHEN @MaxScore  = '' THEN 0 ELSE @MaxScore END;

LOAD DATA INFILE '/ProgramData/MySQL/MySQL Server 5.7/etc/SupernaturalCMS/Datasets/Processed/MEDITATION_WORKOUTS.csv' 
	IGNORE INTO TABLE Meditation
	FIELDS TERMINATED BY ','
	ENCLOSED BY '"'
	LINES TERMINATED BY '\r\n'
	IGNORE 1 LINES
	(@WorkoutId)
    SET WorkoutId=@WorkoutId;

LOAD DATA INFILE '/ProgramData/MySQL/MySQL Server 5.7/etc/SupernaturalCMS/Datasets/Processed/STRETCHING_WORKOUTS.csv' 
	IGNORE INTO TABLE STRETCH
	FIELDS TERMINATED BY ','
	ENCLOSED BY '"'
	LINES TERMINATED BY '\r\n'
	IGNORE 1 LINES
	(@WorkoutId)
    SET WorkoutId=@WorkoutId;

LOAD DATA INFILE '/ProgramData/MySQL/MySQL Server 5.7/etc/SupernaturalCMS/Datasets/Processed/GENRES.csv' 
	IGNORE INTO TABLE Genres
	FIELDS TERMINATED BY ','
	ENCLOSED BY '"'
	LINES TERMINATED BY '\r\n'
	IGNORE 1 LINES
	(@Name, @GenreId)
	SET GenreId=@GenreId, Name=@Name;

LOAD DATA INFILE '/ProgramData/MySQL/MySQL Server 5.7/etc/SupernaturalCMS/Datasets/Processed/GENRE_LIST.csv' 
	IGNORE INTO TABLE GenreList
	FIELDS TERMINATED BY ','
	ENCLOSED BY '"'
	LINES TERMINATED BY '\r\n'
	IGNORE 1 LINES
	(@WorkoutId, @GenreId)
	SET WorkoutId=@WorkoutId, GenreId=@GenreId;

LOAD DATA INFILE '/ProgramData/MySQL/MySQL Server 5.7/etc/SupernaturalCMS/Datasets/Processed/SONGS.csv' 
	IGNORE INTO TABLE Songs
	FIELDS TERMINATED BY ','
	ENCLOSED BY '"'
	LINES TERMINATED BY '\r\n'
	IGNORE 1 LINES
	(@SongName, @Artist, @Length, @Song_Sn_Id)
	SET SongId=@Song_Sn_Id, Name=@SongName, Artist=@Artist, Length=@Length; 


LOAD DATA INFILE '/ProgramData/MySQL/MySQL Server 5.7/etc/SupernaturalCMS/Datasets/Processed/LOCATIONS.csv' 
	INTO TABLE Locations
	FIELDS TERMINATED BY ','
	ENCLOSED BY '"'
	# Windows platforms may need '\r\n'
	LINES TERMINATED BY '\r\n'
	IGNORE 1 LINES
    (@Name,@ScreenshotUrl,@SnId,@NearGround)
    SET Name=@Name, ScreenshotUrl=@ScreenshotUrl, LocationId=@SnId,
    NearGround= CASE WHEN @NearGround = 'checked' THEN 
		True 
    ELSE 
		False 
    END;



LOAD DATA INFILE '/ProgramData/MySQL/MySQL Server 5.7/etc/SupernaturalCMS/Datasets/Processed/SONG_MAP_LIST.csv' 
	INTO TABLE SongMaps
	FIELDS TERMINATED BY ','
	ENCLOSED BY '"'
	# Windows platforms may need '\r\n'
	LINES TERMINATED BY '\r\n'
	IGNORE 1 LINES
    (@WorkoutId,@SongId,@LocationId)
    SET WorkoutId=@WorkoutId, SongId=@SongId, LocationId=@LocationId;