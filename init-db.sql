-- Create tables

CREATE TABLE sport (
	id VARCHAR(255) PRIMARY KEY,
	name VARCHAR(255),
	url VARCHAR(255),
	odf_code VARCHAR(100),
	pictogram VARCHAR(255)
);

CREATE TABLE event (
	id bigint PRIMARY KEY,
	name VARCHAR(255),
	sport VARCHAR(255),
	CONSTRAINT fk_sport
		FOREIGN KEY (sport)
			REFERENCES sport(id)
);

CREATE TABLE season (
	id VARCHAR(255) PRIMARY KEY,
	name VARCHAR(255)
);

CREATE TABLE edition (
	id VARCHAR(255) PRIMARY KEY,
	season VARCHAR(255),
	name VARCHAR(255),
	map jsonb,
	date VARCHAR(255),
	country VARCHAR(255),
	athletes int,
	teams int,
	events int,
	CONSTRAINT fk_season
		FOREIGN KEY (season)
			REFERENCES season(id)
);

CREATE TABLE sport_in_edition (
	id_sport VARCHAR(255),
	id_edition VARCHAR(255),
	PRIMARY KEY (id_sport, id_edition),
	CONSTRAINT fk_rel_sport_of_edition
		FOREIGN KEY (id_sport)
			REFERENCES sport(id),
	CONSTRAINT fk_rel_edition_of_sport
		FOREIGN KEY (id_edition)
			REFERENCES edition(id)
);

CREATE TABLE sport_in_season (
	id_sport VARCHAR(255),
	id_season VARCHAR(255),
	PRIMARY KEY (id_sport, id_season),
	CONSTRAINT fk_rel_sport_of_season
		FOREIGN KEY (id_sport)
			REFERENCES sport(id),
	CONSTRAINT fk_rel_season_of_sport
		FOREIGN KEY (id_season)
			REFERENCES season(id)
);