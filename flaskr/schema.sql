DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS user_ratings;
DROP TABLE IF EXISTS genre;

CREATE TABLE user (
	Id INTEGER PRIMARY KEY AUTOINCREMENT,
	Age INTEGER NULL,
	Gender TEXT NULL,
	Occupation TEXT NULL,
	Zip_Code TEXT NULL,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL
);


CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (Id)
);

CREATE TABLE genre (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name Text NOT NULL
);

CREATE TABLE movies (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	Title TEXT NOT NULL,
	release_date TIMESTAMP,
	video_release_date TIMESTAMP,
	IMDB_URL TEXT,
	Image_URL TEXT NULL,
	unknown INTEGER,
	action INTEGER,
	adventure INTEGER,
	animation INTEGER,
	childrens INTEGER,
	comedy INTEGER,
	crime INTEGER,
	documentary INTEGER,
	drama INTEGER,
	fantasy INTEGER,
	[film-noir] INTEGER,
	horror INTEGER,
	musical INTEGER,
	mystery INTEGER,
	romance INTEGER,
	[Sci-Fi] INTEGER,
	thriller INTEGER,
	war INTEGER,
	western INTEGER
);

CREATE TABLE user_ratings (
	user_id INTEGER,
	item_id INTEGER,
	rating INTEGER,
	timestamp TIMESTAMP,
	FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(item_id) REFERENCES movies(id)
);