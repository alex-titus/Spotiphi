LOAD DATA LOCAL INFILE 'C:/Users/Alex/Documents/GitHub/Spotiphi/output/audio_features_file.csv' 
INTO TABLE audio_features
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;